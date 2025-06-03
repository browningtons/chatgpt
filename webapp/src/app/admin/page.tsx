'use client';
import { useEffect, useState } from 'react';

export default function Admin() {
  const [pw, setPw] = useState('');
  const [authed, setAuthed] = useState(false);
  const [bookings, setBookings] = useState<any[]>([]);

  const load = async () => {
    const res = await fetch('/api/bookings');
    if (res.ok) setBookings(await res.json());
  };

  useEffect(() => {
    if (authed) load();
  }, [authed]);

  if (!authed) {
    return (
      <div className="space-y-4 max-w-md mx-auto">
        <h2 className="text-xl font-bold">Admin Login</h2>
        <input type="password" value={pw} onChange={e => setPw(e.target.value)} className="border p-2 w-full" />
        <button onClick={() => setAuthed(pw === process.env.NEXT_PUBLIC_ADMIN_PASSWORD)} className="bg-green-700 text-white px-4 py-2 rounded">Enter</button>
      </div>
    );
  }

  return (
    <div className="space-y-4 max-w-md mx-auto">
      <h2 className="text-2xl font-bold">Bookings</h2>
      <ul className="space-y-2">
        {bookings.map((b, i) => (
          <li key={i} className="border p-2">
            <div>{b.date} {b.time}</div>
            <div>{b.services.join(', ')}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
