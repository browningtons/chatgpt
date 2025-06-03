import Link from "next/link";

export default function Header() {
  return (
    <header className="bg-green-700 text-white p-4 flex justify-between items-center">
      <h1 className="font-bold text-lg">Graham and Easton's Landscaping</h1>
      <nav className="space-x-4">
        <Link href="/" className="hover:underline">Home</Link>
        <Link href="/services" className="hover:underline">Services</Link>
        <Link href="/booking" className="hover:underline">Book</Link>
        <Link href="/admin" className="hover:underline">Admin</Link>
      </nav>
    </header>
  );
}
