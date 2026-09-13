import { useEffect, useState } from "react";
import { Box, Typography, TextField, MenuItem } from "@mui/material";

import MainLayout from "../layouts/MainLayout";
import RestaurantCard from "../components/RestaurantCard";
import api from "../api/api";

type Restaurant = {
  id: number;
  name: string;
  address: string;
  category_name: string;
  average_rating: number;
  total_reviews: number;
};

export default function Restaurants() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [search, setSearch] = useState("");
  const [location, setLocation] = useState("");
  const [category, setCategory] = useState("");
  const [sortBy, setSortBy] = useState("");
  const [categories, setCategories] = useState<any[]>([]);

async function fetchRestaurants() {
  const response = await api.get("/restaurants", {
    params: {
      name: search || undefined,
    },
  });

  setRestaurants(response.data);
}
async function loadCategories() {
  const response = await api.get("/categories");
  setCategories(response.data);
}


  useEffect(() => {
    fetchRestaurants();
    loadCategories();
  }, []);
  const filteredRestaurants = restaurants
    .filter((restaurant) =>
      restaurant.name.toLowerCase().includes(search.toLowerCase())
    )
    .filter((restaurant) =>
      restaurant.address.toLowerCase().includes(location.toLowerCase())
    )
    .filter((restaurant) =>
      category ? restaurant.category_name === category : true
    )
    .sort((a, b) => {
      if (sortBy === "rating") {
        return b.average_rating - a.average_rating;
      }

      return 0;
    });
  return (
    <MainLayout>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 700 }}>
          Restaurants
        </Typography>

        <Typography color="text.secondary">
          Search and discover restaurants.
        </Typography>
      </Box>

      <Box sx={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 2, mb: 4 }}>
        <TextField
          label="Search by name"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          fullWidth
        />

        <TextField
          label="Location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          fullWidth
        />

        <TextField
          select
          label="Category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          fullWidth
        >
        <MenuItem value="">All</MenuItem>

        {categories.map((categoryItem) => (
          <MenuItem key={categoryItem.id} value={categoryItem.name}>
            {categoryItem.name}
          </MenuItem>
        ))}
        </TextField>

        <TextField
          select
          label="Sort"
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          fullWidth
        >
          <MenuItem value="">Default</MenuItem>
          <MenuItem value="rating">Highest Rating</MenuItem>
        </TextField>
      </Box>
      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
          gap: 3,
        }}
      >
        {filteredRestaurants.map((restaurant) => (
          <RestaurantCard
            key={restaurant.id}
            restaurant={restaurant}
          />
        ))}
      </Box>
    </MainLayout>
  );
}