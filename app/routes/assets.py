import csv
from io import StringIO

from flask import Blueprint, Response, jsonify, request
from app import db
from app.models import Asset, AssetStatusChange

assets_bp = Blueprint('assets', __name__, url_prefix='/api')

PER_PAGE = 10


def _asset_filters():
    return {
        'search': request.args.get('search', '').strip(),
        'type': request.args.get('type', '').strip(),
        'status': request.args.get('status', '').strip(),
    }


def _build_asset_query(filters=None):
    filters = filters or _asset_filters()

    query = Asset.query

    if filters['search']:
        query = query.filter(Asset.name.ilike(f"%{filters['search']}%"))

    if filters['type']:
        query = query.filter(Asset.asset_type == filters['type'])

    if filters['status']:
        query = query.filter(Asset.status == filters['status'])

    return query


def _requester_ip():
    forwarded_for = request.headers.get('X-Forwarded-For', '')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.remote_addr or 'unknown'


def _log_status_change(asset, previous_status, new_status):
    if previous_status == new_status:
        return

    db.session.add(AssetStatusChange(
        asset_id=asset.id,
        previous_status=previous_status,
        new_status=new_status,
        requester_ip=_requester_ip(),
    ))


@assets_bp.route('/assets', methods=['GET'])
def list_assets():
    page = request.args.get('page', 1, type=int)
    query = _build_asset_query()

    total = query.count()

    offset = (page - 1) * PER_PAGE
    assets = query.order_by(Asset.name).offset(offset).limit(PER_PAGE).all()

    return jsonify({
        'assets': [a.to_dict() for a in assets],
        'total': total,
        'page': page,
        'per_page': PER_PAGE,
        'pages': max(1, (total + PER_PAGE - 1) // PER_PAGE),
    })


@assets_bp.route('/assets/export', methods=['GET'])
def export_assets():
    assets = _build_asset_query().order_by(Asset.name).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'ID',
        'Name',
        'Type',
        'Status',
        'Client',
        'Serial Number',
        'Assigned To',
        'Last Seen',
        'Notes',
        'Created At',
    ])

    for asset in assets:
        writer.writerow([
            asset.id,
            asset.name,
            asset.asset_type,
            asset.status,
            asset.client.name if asset.client else '',
            asset.serial_number or '',
            asset.assigned_to or '',
            asset.last_seen.isoformat() if asset.last_seen else '',
            asset.notes or '',
            asset.created_at.isoformat(),
        ])

    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=assets.csv'},
    )


@assets_bp.route('/assets/<int:asset_id>', methods=['GET'])
def get_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    return jsonify(asset.to_dict())


@assets_bp.route('/assets/<int:asset_id>/audit', methods=['GET'])
def get_asset_audit(asset_id):
    Asset.query.get_or_404(asset_id)
    changes = AssetStatusChange.query.filter_by(asset_id=asset_id).order_by(AssetStatusChange.created_at.desc()).all()
    return jsonify({'audit': [change.to_dict() for change in changes]})


@assets_bp.route('/assets', methods=['POST'])
def create_asset():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    name = data.get('name', '').strip()
    asset_type = data.get('asset_type', '').strip()
    client_id = data.get('client_id')

    if not name or not asset_type or not client_id:
        return jsonify({'error': 'Name, asset type, and client_id are required'}), 400

    asset = Asset(
        name=name,
        asset_type=asset_type,
        client_id=client_id,
        serial_number=data.get('serial_number'),
        assigned_to=data.get('assigned_to'),
        notes=data.get('notes'),
        status=data.get('status', 'active'),
    )
    db.session.add(asset)
    db.session.commit()
    return jsonify(asset.to_dict()), 201


@assets_bp.route('/assets/<int:asset_id>', methods=['PUT'])
def update_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    if 'name' in data:
        asset.name = data['name']
    if 'asset_type' in data:
        asset.asset_type = data['asset_type']
    if 'serial_number' in data:
        asset.serial_number = data['serial_number']
    if 'assigned_to' in data:
        asset.assigned_to = data['assigned_to']
    if 'notes' in data:
        asset.notes = data['notes']
    if 'client_id' in data:
        asset.client_id = data['client_id']

    db.session.commit()
    return jsonify(asset.to_dict())


@assets_bp.route('/assets/<int:asset_id>', methods=['DELETE'])
def delete_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    db.session.delete(asset)
    db.session.commit()
    return jsonify({'message': 'Asset deleted'}), 200


@assets_bp.route('/assets/<int:asset_id>/toggle', methods=['POST'])
def toggle_asset_status(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    previous_status = asset.status

    if asset.status == 'active':
        asset.status = 'inactive'
    elif asset.status == 'inactive':
        asset.status = 'active'
    # retired assets cannot be toggled further

    _log_status_change(asset, previous_status, asset.status)
    db.session.commit()
    return jsonify(asset.to_dict())


@assets_bp.route('/assets/<int:asset_id>/decommission', methods=['POST'])
def decommission_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    if asset.status == 'retired':
        return jsonify({'error': 'Asset is already retired'}), 400
    previous_status = asset.status
    asset.status = 'retired'
    _log_status_change(asset, previous_status, asset.status)
    db.session.commit()
    return jsonify(asset.to_dict())
