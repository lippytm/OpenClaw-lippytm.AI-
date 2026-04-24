from app.state.session_awareness import build_session_snapshot


def test_build_session_snapshot_with_goal():
    snapshot = build_session_snapshot('session_1', current_goal='Route task', memory_summary='Short summary')
    assert snapshot['session_id'] == 'session_1'
    assert snapshot['state'] == 'planning'
    assert snapshot['current_goal'] == 'Route task'


def test_build_session_snapshot_without_goal():
    snapshot = build_session_snapshot('session_2')
    assert snapshot['state'] == 'idle'
