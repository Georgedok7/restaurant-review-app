import { useEffect, useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Paper,
  Typography,
} from "@mui/material";

import MainLayout from "../layouts/MainLayout";
import api from "../api/api";

export default function AdminDashboard() {
  const [stats, setStats] = useState<any>(null);
  const [pendingRestaurants, setPendingRestaurants] = useState<any[]>([]);
  const [reports, setReports] = useState<any[]>([]);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    const statsRes = await api.get("/statistics/admin");
    const pendingRes = await api.get("/restaurants/pending");
    const reportsRes = await api.get("/reports");

    setStats(statsRes.data);
    setPendingRestaurants(pendingRes.data);
    setReports(reportsRes.data);
  }

  async function approveRestaurant(id: number) {
    await api.put(`/restaurants/${id}/approve`);
    await loadData();
  }

  async function rejectRestaurant(id: number) {
    const reason = prompt("Rejection reason:");

    if (!reason) return;

    await api.put(`/restaurants/${id}/reject`, {
      rejection_reason: reason,
    });

    await loadData();
  }

  async function closeReport(id: number) {
    await api.put(`/reports/${id}/close`);
    await loadData();
  }

  return (
    <MainLayout>
      <Typography variant="h4" sx={{ fontWeight: 700, mb: 4 }}>
        Admin Dashboard
      </Typography>

      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
          gap: 3,
          mb: 5,
        }}
      >
        <Card>
          <CardContent>
            <Typography>Total Users</Typography>
            <Typography variant="h4">{stats?.total_users ?? "-"}</Typography>
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <Typography>Restaurants</Typography>
            <Typography variant="h4">{stats?.total_restaurants ?? "-"}</Typography>
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <Typography>Reviews</Typography>
            <Typography variant="h4">{stats?.total_reviews ?? "-"}</Typography>
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <Typography>Reports</Typography>
            <Typography variant="h4">{stats?.total_reports ?? "-"}</Typography>
          </CardContent>
        </Card>
      </Box>

      <Typography variant="h5" sx={{ fontWeight: 700, mb: 2 }}>
        Pending Restaurants
      </Typography>

      {pendingRestaurants.length === 0 && (
        <Typography color="text.secondary" sx={{ mb: 3 }}>
          No pending restaurants.
        </Typography>
      )}

      {pendingRestaurants.map((restaurant) => (
        <Paper key={restaurant.id} sx={{ p: 3, mb: 2 }}>
          <Typography variant="h6" sx={{ fontWeight: 700 }}>
            {restaurant.name}
          </Typography>

          <Typography color="text.secondary">
            {restaurant.address}
          </Typography>

          <Typography sx={{ mt: 1 }}>
            {restaurant.description}
          </Typography>

          <Box sx={{ display: "flex", gap: 1, mt: 2 }}>
            <Button
              variant="contained"
              onClick={() => approveRestaurant(restaurant.id)}
            >
              Approve
            </Button>

            <Button
              color="error"
              variant="outlined"
              onClick={() => rejectRestaurant(restaurant.id)}
            >
              Reject
            </Button>
          </Box>
        </Paper>
      ))}

        <Typography variant="h5" sx={{ fontWeight: 700, mt: 5, mb: 2 }}>
        Reports ({reports.length})
        </Typography>

      {reports.length === 0 && (
        <Typography color="text.secondary">
          No reports.
        </Typography>
      )}

        {reports.map((report) => (
        <Paper key={report.id} sx={{ p: 3, mb: 2 }}>
            <Typography variant="h6" sx={{ fontWeight: 700 }}>
            Report #{report.id}
            </Typography>

            <Typography sx={{ mt: 1 }}>
            <strong>Review ID:</strong> {report.review_id}
            </Typography>

            <Typography>
            <strong>Reason:</strong> {report.reason}
            </Typography>

            <Typography
            sx={{ mt: 1 }}
            color={report.status === "closed" ? "success.main" : "error.main"}
            >
            <strong>Status:</strong> {report.status}
            </Typography>

            <Box sx={{ mt: 2 }}>
            {report.status !== "closed" ? (
                <Button
                variant="contained"
                color="success"
                onClick={() => closeReport(report.id)}
                >
                Close Report
                </Button>
            ) : (
                <Button variant="outlined" disabled>
                Closed
                </Button>
            )}
            </Box>
        </Paper>
        ))}
    </MainLayout>
  );
}