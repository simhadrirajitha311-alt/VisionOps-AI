import { useEffect, useMemo, useState } from 'react';

type EventItem = {
  id?: number | string;
  event_type: string;
  severity: string;
  object_class?: string;
  track_id?: number | null;
  zone?: string | null;
  confidence?: number | null;
  timestamp?: string;
  status?: string;
  metadata?: Record<string, unknown>;
};

type SystemStatusResponse = {
  status: string;
  camera: {
    status: string;
    source: number | string;
    frame_width: number;
    frame_height: number;
  };
  metrics: Record<string, number | string>;
  objects: number;
  events: number;
  fps: number;
  inference_latency_ms: number;
};

const buildBaseUrl = () => {
  const host = (import.meta.env.VITE_API_BASE_URL as string | undefined) || 'http://localhost:8000';
  return host.endsWith('/') ? host.slice(0, -1) : host;
};

const formatTime = (timestamp?: string) => {
  if (!timestamp) return 'N/A';
  try {
    return new Date(timestamp).toLocaleTimeString();
  } catch {
    return timestamp;
  }
};

export default function App() {
  const [systemStatus, setSystemStatus] = useState<SystemStatusResponse | null>(null);
  const [events, setEvents] = useState<EventItem[]>([]);
  const [selectedEvent, setSelectedEvent] = useState<EventItem | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const [statusRes, eventsRes] = await Promise.all([
          fetch(`${buildBaseUrl()}/api/system/status`),
          fetch(`${buildBaseUrl()}/api/events`),
        ]);

        if (!statusRes.ok || !eventsRes.ok) {
          throw new Error('Unable to contact backend');
        }

        const statusData = await statusRes.json();
        const eventsData = await eventsRes.json();
        setSystemStatus(statusData);
        setEvents(Array.isArray(eventsData) ? eventsData : []);
        if (eventsData.length) setSelectedEvent(eventsData[0]);
      } catch (fetchError) {
        setError(fetchError instanceof Error ? fetchError.message : 'Connection failed');
      }
    };

    fetchStatus();
    const timer = window.setInterval(fetchStatus, 5000);
    return () => window.clearInterval(timer);
  }, []);

  const statusCards = useMemo(
    () => [
      { label: 'System Status', value: systemStatus?.status ?? 'offline' },
      { label: 'Objects', value: String(systemStatus?.objects ?? 0) },
      { label: 'Events', value: String(systemStatus?.events ?? 0) },
      { label: 'FPS', value: String(systemStatus?.fps ?? 0) },
      { label: 'Inference', value: `${systemStatus?.inference_latency_ms ?? 0} ms` },
      { label: 'Camera', value: systemStatus?.camera.status ?? 'offline' },
    ],
    [systemStatus],
  );

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">AI OPERATIONS</p>
          <h1>VISIONOPS AI</h1>
        </div>
        <div className="live-pill">
          <span className="dot" /> LIVE
        </div>
      </header>

      <div className="content-grid">
        <main className="panel main-panel">
          <div className="panel-header">
            <h2>Live Camera</h2>
            <span className="status-badge">{systemStatus?.camera.status ?? 'offline'}</span>
          </div>

          <div className="camera-frame">
            <img
              src={`${buildBaseUrl()}/api/video/stream?ts=${Date.now()}`}
              alt="Live camera preview"
              onError={() => setError('Unable to load live camera stream from backend.')}
            />
          </div>

          <div className="metrics-grid">
            {statusCards.map((card) => (
              <div key={card.label} className="metric-card">
                <div className="metric-label">{card.label}</div>
                <div className="metric-value">{card.value}</div>
              </div>
            ))}
          </div>
        </main>

        <aside className="sidebar">
          <div className="panel">
            <div className="panel-header small">
              <h3>Recent Events</h3>
            </div>
            <div className="event-list">
              {events.length === 0 ? (
                <div className="empty-state">No events yet.</div>
              ) : (
                events.map((event) => (
                  <button
                    key={String(event.id ?? event.event_type + event.timestamp)}
                    className={`event-item severity-${(event.severity || 'medium').toLowerCase()}`}
                    onClick={() => setSelectedEvent(event)}
                  >
                    <div className="event-title">{event.event_type}</div>
                    <div className="event-meta">
                      {event.object_class ?? 'Object'} • {event.track_id ?? 'N/A'}
                    </div>
                    <div className="event-time">{formatTime(event.timestamp)}</div>
                  </button>
                ))
              )}
            </div>
          </div>

          <div className="panel">
            <div className="panel-header small">
              <h3>AI Summary</h3>
            </div>
            <div className="summary-box">
              {selectedEvent ? (
                <>
                  <strong>{selectedEvent.event_type}</strong>
                  <p>
                    Object: {selectedEvent.object_class ?? 'unknown'} | Track: {selectedEvent.track_id ?? 'N/A'} | Confidence: {selectedEvent.confidence ?? 'N/A'}
                  </p>
                  <p>
                    Zone: {selectedEvent.zone ?? 'na'} | Severity: {selectedEvent.severity ?? 'medium'}
                  </p>
                  <p>Evidence: {JSON.stringify(selectedEvent.metadata ?? {}) || 'No metadata available.'}</p>
                </>
              ) : (
                <p>No event selected.</p>
              )}
            </div>
          </div>
        </aside>
      </div>

      {selectedEvent && (
        <section className="detail-panel panel">
          <div className="panel-header small">
            <h3>Event Detail</h3>
          </div>
          <div className="detail-grid">
            <div><label>Event type</label><span>{selectedEvent.event_type}</span></div>
            <div><label>Time</label><span>{formatTime(selectedEvent.timestamp)}</span></div>
            <div><label>Severity</label><span>{selectedEvent.severity}</span></div>
            <div><label>Object</label><span>{selectedEvent.object_class ?? 'N/A'}</span></div>
            <div><label>Track ID</label><span>{selectedEvent.track_id ?? 'N/A'}</span></div>
            <div><label>Confidence</label><span>{selectedEvent.confidence ?? 'N/A'}</span></div>
            <div><label>Zone</label><span>{selectedEvent.zone ?? 'N/A'}</span></div>
            <div><label>Duration</label><span>{String(selectedEvent.metadata?.duration_seconds ?? 'N/A')}</span></div>
            <div className="full-row"><label>Evidence metadata</label><span>{JSON.stringify(selectedEvent.metadata ?? {})}</span></div>
            <div className="full-row"><label>AI explanation</label><span>Observed event facts were used to generate this summary. Interpretations remain separate from the underlying evidence.</span></div>
          </div>
        </section>
      )}

      {error && <div className="error-banner">{error}</div>}
    </div>
  );
}
