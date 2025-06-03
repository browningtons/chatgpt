import { NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';

const BOOKINGS_FILE = path.join(process.cwd(), 'bookings.json');

export async function GET() {
  try {
    const data = await fs.readFile(BOOKINGS_FILE, 'utf8');
    const bookings = data ? JSON.parse(data) : [];
    return NextResponse.json(bookings);
  } catch (e) {
    return NextResponse.json([]);
  }
}

export async function POST(req: Request) {
  const booking = await req.json();
  try {
    const data = await fs.readFile(BOOKINGS_FILE, 'utf8').catch(() => '[]');
    const bookings = data ? JSON.parse(data) : [];
    bookings.push({ ...booking, created: new Date().toISOString() });
    await fs.writeFile(BOOKINGS_FILE, JSON.stringify(bookings, null, 2));

    if (process.env.IFTTT_WEBHOOK_URL) {
      fetch(process.env.IFTTT_WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ value1: booking.date, value2: booking.time, value3: booking.services.join(', ') })
      }).catch(() => {});
    }

    return NextResponse.json({ ok: true });
  } catch (e) {
    return NextResponse.json({ ok: false }, { status: 500 });
  }
}
