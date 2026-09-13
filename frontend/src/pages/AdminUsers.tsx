import { useEffect, useState } from "react";
import {
  Paper,
  Typography,
  Button,
  Box,
} from "@mui/material";

import MainLayout from "../layouts/MainLayout";
import api from "../api/api";

export default function AdminUsers() {
  const [users, setUsers] = useState<any[]>([]);

  async function loadUsers() {
    const response = await api.get("/users");
    setUsers(response.data);
  }

  useEffect(() => {
    loadUsers();
  }, []);

  async function toggleBan(user: any) {
    if (user.is_banned) {
      await api.put(`/users/${user.id}/unban`);
    } else {
      await api.put(`/users/${user.id}/ban`);
    }

    loadUsers();
  }

  return (
    <MainLayout>
      <Typography
        variant="h4"
        sx={{ fontWeight: 700, mb: 4 }}
      >
        User Management
      </Typography>

      {users.map((user) => (
        <Paper
          key={user.id}
          sx={{ p: 3, mb: 2 }}
        >
          <Typography variant="h6">
            {user.first_name} {user.last_name}
          </Typography>

          <Typography>
            {user.email}
          </Typography>

          <Typography>
            Role: {user.role}
          </Typography>

          <Typography
            color={
              user.is_banned
                ? "error.main"
                : "success.main"
            }
          >
            {user.is_banned ? "Banned" : "Active"}
          </Typography>

          <Box sx={{ mt: 2 }}>
            <Button
            variant="contained"
            color={user.is_banned ? "success" : "error"}
            disabled={user.role === "admin"}
            onClick={() => toggleBan(user)}
            >
            {user.is_banned ? "Unban" : "Ban"}
            </Button>
          </Box>
        </Paper>
      ))}
    </MainLayout>
  );
}