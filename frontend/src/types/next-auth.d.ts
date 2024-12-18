// \frontend\src\types\next-auth.d.ts

import NextAuth, { DefaultSession, DefaultUser } from "next-auth";
import "next-auth/jwt";

declare module "next-auth" {
  interface Session {
    user: {
      id: string; // Custom id field
      email: string;
    } & DefaultSession["user"];
    accessToken: string; // Add accessToken to session
  }

  interface User extends DefaultUser {
    id: string; // User id
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    id: string; // Add id to JWT token
    email: string; // Add email to JWT token
    accessToken: string; // Add accessToken to JWT token
  }
}
