import { useEffect, useState } from "react";
import {
  Box,
  Button,
  Paper,
  Typography,
} from "@mui/material";
import { Link } from "react-router-dom";

import MainLayout from "../layouts/MainLayout";
import api from "../api/api";

type Favorite = {
  id: number;
  restaurant_id: number;
  restaurant_name: string;
  restaurant_address: string;
};

export default function Favorites() {
  const [favorites, setFavorites] = useState<Favorite[]>([]);

  async function loadFavorites() {
    const response = await api.get("/favorites");
    setFavorites(response.data);
  }

  async function removeFavorite(restaurantId: number) {
    await api.delete(`/favorites/${restaurantId}`);
    await loadFavorites();
  }

  useEffect(() => {
    loadFavorites();
  }, []);

  return (
    <MainLayout>
      <Typography variant="h4" sx={{ fontWeight: 700, mb: 3 }}>
        My Favorites
      </Typography>

      {favorites.length === 0 && (
        <Typography color="text.secondary">
          You do not have favorite restaurants yet.
        </Typography>
      )}

      <Box sx={{ display: "grid", gap: 2 }}>
        {favorites.map((favorite) => (
          <Paper
            key={favorite.id}
            sx={{
              p: 3,
              borderRadius: 3,
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <Box>
              <Typography variant="h6" sx={{ fontWeight: 700 }}>
                {favorite.restaurant_name}
              </Typography>

              <Typography color="text.secondary">
                📍 {favorite.restaurant_address}
              </Typography>
            </Box>

            <Box sx={{ display: "flex", gap: 1 }}>
              <Button
                component={Link}
                to={`/restaurants/${favorite.restaurant_id}`}
                variant="outlined"
              >
                View
              </Button>

              <Button
                color="error"
                variant="contained"
                onClick={() => removeFavorite(favorite.restaurant_id)}
              >
                Remove
              </Button>
            </Box>
          </Paper>
        ))}
      </Box>
    </MainLayout>
  );
}