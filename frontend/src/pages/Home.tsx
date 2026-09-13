import { Box, Button, Typography, Paper } from "@mui/material";
import { Link } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";

export default function Home() {
  return (
    <MainLayout>
      <Paper sx={{ p: 6, textAlign: "center", borderRadius: 4 }}>
        <Typography
            variant="h3"
            gutterBottom
            sx={{ fontWeight: 700 }}
        >
          Find your next favorite restaurant
        </Typography>

        <Typography variant="h6" color="text.secondary" sx={{ mb: 4 }}>
          Search restaurants, read reviews, save favorites and discover new places.
        </Typography>

      <Box sx={{ display: "flex", gap: 2, justifyContent: "center" }}>
        <Button component={Link} to="/restaurants" variant="contained" size="large">
            Browse Restaurants
        </Button>

        <Button component={Link} to="/login" variant="outlined" size="large">
            Login
        </Button>
      </Box>
      </Paper>

      <Box sx={{ mt: 4 }}>
        <Typography
            variant="h5"
            sx={{ fontWeight: 700 }}
        >
          Welcome to Restaurant Reviews
        </Typography>
        <Typography color="text.secondary" sx={{ mt: 1 }}>
          A simple platform for customers, restaurant owners and administrators.
        </Typography>
      </Box>
    </MainLayout>
  );
}