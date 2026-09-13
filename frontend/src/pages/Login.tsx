import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import {
  Box,
  Button,
  Paper,
  TextField,
  Typography,
  Alert,
} from "@mui/material";

import MainLayout from "../layouts/MainLayout";
import { useAuth } from "../contexts/AuthContext";
import api from "../api/api";

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [email, setEmail] = useState("customer@test.com");
  const [password, setPassword] = useState("12345678");
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    try {
      setError("");
        await login(email, password);

        const me = await api.get("/auth/me");

        switch (me.data.role) {
        case "admin":
            navigate("/admin");
            break;

        case "owner":
            navigate("/owner");
            break;

        default:
            navigate("/restaurants");
        }
    } catch {
      setError("Invalid email or password.");
    }
  }

  return (
    <MainLayout>
      <Box sx={{ maxWidth: 420, mx: "auto" }}>
        <Paper sx={{ p: 4, borderRadius: 3 }}>
          <Typography variant="h4" sx={{ fontWeight: 700, mb: 3 }}>
            Login
          </Typography>

          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

          <Box component="form" onSubmit={handleSubmit}>
            <TextField
              label="Email"
              fullWidth
              sx={{ mb: 2 }}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <TextField
              label="Password"
              type="password"
              fullWidth
              sx={{ mb: 3 }}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <Button type="submit" variant="contained" fullWidth>
              Login
            </Button>
          </Box>

          <Typography sx={{ mt: 2 }}>
            No account? <Link to="/register">Register here</Link>
          </Typography>
        </Paper>
      </Box>
    </MainLayout>
  );
}