import { useEffect, useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Grid,
  Typography,
} from "@mui/material";

import { Link } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import api from "../api/api";

export default function OwnerDashboard() {
  const [restaurants, setRestaurants] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    const restaurantsResponse = await api.get("/restaurants/my");
    console.log(restaurantsResponse.data);
    setRestaurants(restaurantsResponse.data);

    const statsResponse = await api.get("/statistics/owner");
    setStats(statsResponse.data);
    
  }

  return (
    <MainLayout>
        <Box>
        <Typography
        variant="h4"
        sx={{
            fontWeight: 700,
            mb: 4,
        }}
        >
        Owner Dashboard
        </Typography>

        <Grid container spacing={3}>

        <Grid size={{ xs: 12, md: 4 }}>

        <Card>

        <CardContent>

        <Typography variant="h6">
        Restaurants
        </Typography>

        <Typography variant="h3">
        {restaurants.length}
        </Typography>

        </CardContent>

        </Card>

        </Grid>

        <Grid size={{ xs: 12, md: 4 }}>

        <Card>

        <CardContent>

        <Typography variant="h6">
        Average Rating
        </Typography>

        <Typography variant="h3">
        {stats?.average_rating ?? "-"}
        </Typography>

        </CardContent>

        </Card>

        </Grid>

        <Grid size={{ xs: 12, md: 4 }}>

        <Card>

        <CardContent>

        <Typography variant="h6">
        Reviews
        </Typography>

        <Typography variant="h3">
        {stats?.total_reviews ?? "-"}
        </Typography>

        </CardContent>

        </Card>

        </Grid>

        </Grid>

        <Typography
        variant="h5"
        sx={{
            mt: 6,
            mb: 3,
        }}
        >
        My Restaurants
        </Typography>

        <Grid container spacing={3}>

        {restaurants.map((restaurant) => (

        <Grid
        key={restaurant.id}
        size={{ xs: 12, md: 6 }}
        >

        <Card>

        <CardContent>

        <Typography
          variant="h6"
          sx={{
            fontWeight: 700,
          }}
        >
          {restaurant.name}
        </Typography>

        <Typography color="text.secondary">
          📍 {restaurant.address}
        </Typography>

        <Typography color="text.secondary">
          Status: {restaurant.status}
        </Typography>

        <Button
        component={Link}
        to={`/owner/restaurants/${restaurant.id}`}
        variant="contained"
        sx={{ mt: 2 }}
        >
        Manage
        </Button>

        </CardContent>

        </Card>

        </Grid>

        ))}

        </Grid>

        <Button
        component={Link}
        to="/owner/create"
        variant="contained"
        sx={{ mt: 4 }}
        >
        Add Restaurant
        </Button>

        </Box>

    </MainLayout>
  );
}