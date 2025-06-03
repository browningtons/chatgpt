'use client';
import { useState } from 'react';

const SERVICES = [
  'Lawn mowing',
  'Garden maintenance',
  'Seasonal cleanup',
  'Weed wacking',
  'Custom packages'
];

export default function Booking() {
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [services, setServices] = useState<string[]>([]);
  const [message, setMessage] = useState('');

  const times = Array.from({ length: 24 * 2 }, (_, i) => {
    const hour = Math.floor(i / 2);
    const min = i % 2 === 0 ? '00' : '30';
    return `${hour.toString().padStart(2, '0')}:${min}`;
  });

  const toggleService = (s: string) => {
    setServices((prev) =>
      prev.includes(s) ? prev.filter((p) => p !== s) : [...prev, s]
    );
  };

  const submit = async () => {
    const res = await fetch('/api/bookings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date, time, services })
    });
    if (res.ok) {
      setMessage('Booking saved!');
      setDate('');
      setTime('');
      setServices([]);
    } else {
      setMessage('Error saving booking');
    }
  };

  return (
    <div className="space-y-4 max-w-md mx-auto">
      <h2 className="text-2xl font-bold text-green-700">Book a Service</h2>
      <label className="block">
        <span>Date</span>
        <input type="date" value={date} onChange={(e) => setDate(e.target.value)} className="border p-2 w-full" />
      </label>
      <label className="block">
        <span>Time</span>
        <select value={time} onChange={(e) => setTime(e.target.value)} className="border p-2 w-full">
          <option value="">Select...</option>
          {times.map(t => <option key={t}>{t}</option>)}
        </select>
      </label>
      <fieldset>
        <legend>Services</legend>
        {SERVICES.map(s => (
          <label key={s} className="block">
            <input
              type="checkbox"
              checked={services.includes(s)}
              onChange={() => toggleService(s)}
              className="mr-2"
            />
            {s}
          </label>
        ))}
      </fieldset>
      <button onClick={submit} className="bg-green-700 text-white px-4 py-2 rounded">Submit</button>
      {message && <p>{message}</p>}
    </div>
  );
}
