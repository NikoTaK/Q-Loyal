import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = "https://zeobhsiccihwxxhlogfg.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inplb2Joc2ljY2lod3h4aGxvZ2ZnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIzNDkzNzYsImV4cCI6MjA3NzkyNTM3Nn0.mwYydW-dVI5W5jOtV2QcQIEjZu3XUK0PbB5fam6WdkI";  // safe for frontend

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

window.login = async function () {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  const output = document.getElementById("output");

  if (error) {
    output.innerText = "Login error:\n" + JSON.stringify(error, null, 2);
    return;
  }

  const token = data.session.access_token;

  output.innerText =
    "🎉 Logged in!\n\nJWT:\n" +
    token +
    "\n\nNow call your backend with:\n" +
    `curl -H "Authorization: Bearer ${token}" http://localhost:8000/api/me`;

  console.log("JWT:", token);
};
