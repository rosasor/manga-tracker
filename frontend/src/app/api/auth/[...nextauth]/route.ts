// \frontend\src\app\api\auth\[...nextauth]\route.ts

import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import axios from "axios";
import jwt from "jsonwebtoken"; // Import jsonwebtoken


type User = {
  id: string;
  email: string;
  username: string;
};


const authHandler = NextAuth({
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        try {
          const res = await axios.post("http://127.0.0.1:5000/api/login", {
            email: credentials?.email,
            password: credentials?.password,
          });
          if (res.data) {
            return res.data.user; // Return user object on success
          }
          return null;
        } catch (error) {
          console.error("Authorization error:", error);
          return null;
        }
      },
    }),
  ],
  pages: {
    signIn: "/auth/signin",
  },
  session: {
    strategy: "jwt",
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id as string; // Ensure id is string
        token.email = user.email || ""; // Fallback to empty string
        token.accessToken = jwt.sign(
          { id: user.id, email: user.email },
          "KB7xdcAXNEkx6R8XbVqlXG5svYCQkvsy6hMkaEVf7QA", // SECRET_KEY
          { algorithm: "HS256", expiresIn: "1h" }
        );
      }
      return token;
    },
    async session({ session, token }) {
      session.user.id = token.id;
      session.accessToken = token.accessToken; // Add JWT to session
      return session;
    },
  },
});

// Named export for the HTTP method
export { authHandler as GET, authHandler as POST };
