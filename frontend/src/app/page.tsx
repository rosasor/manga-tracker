"use client"

import Link from "next/link";
import { useSession, signOut } from "next-auth/react";

export default function Home() {
  const { data: session } = useSession();

  const handleLogout = async () => {
    await signOut({ callbackUrl: "/" });
  };

  return (
    <div>
      <h1>Welcome to the Manga Tracker</h1>
      {session ? (
        <div>
          <nav>
            <Link href="/">Home</Link>
            <Link href="/manga">Manga Search</Link>
          </nav>
          <p>Logged in as {session.user?.email}</p>
          <button onClick={handleLogout}>Log Out</button>
        </div>
      ) : (
        <div>
          <p>Please log in to continue.</p>
          <nav>
            <Link href="/">Home</Link>
            <Link href="/auth/signin">Sign In</Link>
            <Link href="/auth/signup">Sign Up</Link>
            {/* <Link href="/manga">Manga Search</Link> */}

          </nav>
          <main>{}</main>
        </div>
      )}
    </div>
  );
}
