import { useEffect, useState } from "react";
import {
  Avatar,
  Box,
  Button,
  Paper,
  TextField,
  Typography,
} from "@mui/material";

import MainLayout from "../layouts/MainLayout";
import api from "../api/api";

export default function Profile() {
  const [user, setUser] = useState<any>(null);
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [profileImage, setProfileImage] = useState("");

  useEffect(() => {
    async function loadUser() {
      const response = await api.get("/auth/me");
      setUser(response.data);
      setFirstName(response.data.first_name);
      setLastName(response.data.last_name);
      setProfileImage(response.data.profile_image || "");
    }

    loadUser();
  }, []);

  if (!user) {
    return (
      <MainLayout>
        Loading...
      </MainLayout>
    );
  }
  async function saveProfile() {
    await api.put("/auth/me", {
        first_name: firstName,
        last_name: lastName,
    });

    const response = await api.get("/auth/me");
    setUser(response.data);
    setProfileImage(response.data.profile_image || "");
    }
return (
    <MainLayout>
      <Paper sx={{ p: 4, maxWidth: 650, mx: "auto" }}>
        <Typography
          variant="h4"
          sx={{ fontWeight: 700, mb: 4 }}
        >
          My Profile
        </Typography>

        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 3,
            mb: 4,
          }}
        >
            <Avatar
                src={profileImage}
                sx={{
                    width: 120,
                    height: 120,
                }}
            />

            <TextField
                label="Profile Image URL"
                value={profileImage}
                onChange={(e) => setProfileImage(e.target.value)}
                fullWidth
            />

            <Button
                variant="contained"
                onClick={async () => {
                    await api.put("/auth/me/profile-image", {
                        profile_image: profileImage,
                    });

                    const response = await api.get("/auth/me");

                    setUser(response.data);
                    setProfileImage(response.data.profile_image || "");
                }}
            >
                Save Photo
            </Button>
        </Box>

        <TextField
          label="First Name"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          fullWidth
          sx={{ mb: 2 }}
        />

        <TextField
          label="Last Name"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          fullWidth
          sx={{ mb: 2 }}
        />

        <TextField
          label="Email"
          value={user.email}
          fullWidth
          sx={{ mb: 2 }}
        />

        <TextField
          label="Role"
          value={user.role}
          fullWidth
        />

      <Button
        variant="contained"
        sx={{ mt: 3 }}
        onClick={saveProfile}
      >
        Save Changes
      </Button>
      </Paper>
    </MainLayout>
  );
}