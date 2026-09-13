import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Rating,
  MenuItem
} from "@mui/material";

import MainLayout from "../layouts/MainLayout";
import api from "../api/api";

export default function OwnerRestaurantManage() {
  const { id } = useParams();

  const [restaurant, setRestaurant] = useState<any>(null);
  const [stats, setStats] = useState<any>(null);
  const [images, setImages] = useState<any[]>([]);
  const [reviews, setReviews] = useState<any[]>([]);
  const [newImage, setNewImage] = useState("");
  const [categories, setCategories] = useState<any[]>([]);
  useEffect(() => {
    loadData();
  }, [id]);

  async function loadData() {
    const restaurantRes = await api.get(`/restaurants/${id}`);
    const statsRes = await api.get(`/statistics/restaurant/${id}`);
    const imagesRes = await api.get(`/restaurants/${id}/images`);
    const reviewsRes = await api.get(`/reviews/restaurant/${id}`);
    const categoriesRes = await api.get("/categories");
    
    setCategories(categoriesRes.data);
    setRestaurant(restaurantRes.data);
    setStats(statsRes.data);
    setImages(imagesRes.data);
    setReviews(reviewsRes.data);
  }

  if (!restaurant) {
    return (
      <MainLayout>
        Loading...
      </MainLayout>
    );
  }
  async function saveRestaurant() {
  await api.put(`/restaurants/${id}`, {
        category_id: restaurant.category_id,
        name: restaurant.name,
        description: restaurant.description,
        address: restaurant.address,
        phone: restaurant.phone,
        opening_hours: restaurant.opening_hours,
    });

    alert("Restaurant updated successfully!");
    }
    async function uploadImage() {
        await api.post(`/restaurants/${id}/images`, {
            image_url: newImage,
        });

        const response = await api.get(`/restaurants/${id}/images`);

        setImages(response.data);

        setNewImage("");
    }

  return (
    <MainLayout>
      <Typography variant="h4" sx={{ fontWeight: 700, mb: 3 }}>
        Manage {restaurant.name}
      </Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6">Statistics</Typography>
        <Typography>Reviews: {stats?.total_reviews}</Typography>
        <Typography>Average Rating: {stats?.average_rating}</Typography>
        <Typography>Total Views: {stats?.total_views}</Typography>
        <Typography>Monthly Views: {stats?.monthly_views}</Typography>
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Restaurant Info
        </Typography>

        <TextField
        label="Name"
        value={restaurant.name}
        onChange={(e) =>
            setRestaurant({ ...restaurant, name: e.target.value })
        }
        fullWidth
        sx={{ mb: 2 }}
        />        
        <TextField
          select
          label="Category"
          value={restaurant.category_id}
          onChange={(e) =>
            setRestaurant({
              ...restaurant,
              category_id: Number(e.target.value),
            })
          }
          fullWidth
          sx={{ mb: 2 }}
        >
          {categories.map((category) => (
            <MenuItem key={category.id} value={category.id}>
              {category.name}
            </MenuItem>
          ))}
        </TextField>

        <TextField
          label="Description"
          value={restaurant.description}
          onChange={(e) =>
            setRestaurant({ ...restaurant, description: e.target.value })
          }
          fullWidth
          sx={{ mb: 2 }}
        />
        <TextField
        label="Address"
        value={restaurant.address}
        onChange={(e) =>
            setRestaurant({ ...restaurant, address: e.target.value })
        }
        fullWidth
        sx={{ mb: 2 }}
        />
        <TextField
        label="Phone"
        value={restaurant.phone}
        onChange={(e) =>
            setRestaurant({ ...restaurant, phone: e.target.value })
        }
        fullWidth
        sx={{ mb: 2 }}
        />        
        <TextField
        label="Opening Hours"
        value={restaurant.opening_hours}
        onChange={(e) =>
            setRestaurant({ ...restaurant, opening_hours: e.target.value })
        }
        fullWidth
        />
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Images
        </Typography>

        <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap" }}>
          {images.map((image) => (
            <Box
              key={image.id}
              component="img"
              src={image.image_url}
              sx={{
                width: 180,
                height: 120,
                objectFit: "cover",
                borderRadius: 2,
              }}
            />
          ))}
        </Box>
        <Box sx={{ mt: 3 }}>
            <TextField
                label="Image URL"
                value={newImage}
                onChange={(e) => setNewImage(e.target.value)}
                fullWidth
                sx={{ mb: 2 }}
            />

            <Button
                variant="contained"
                onClick={uploadImage}
            >
                Add Image
            </Button>
        </Box>
      </Paper>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Reviews
        </Typography>

        {reviews.map((review) => (
          <Box key={review.id} sx={{ mb: 3 }}>
            <Rating value={review.rating} readOnly />
            <Typography>{review.comment}</Typography>

        {!review.reply && (
          <Button
            variant="outlined"
            sx={{ mt: 2 }}
            onClick={async () => {
              const reply = prompt("Write your reply:");

              if (!reply) return;

              await api.post(`/review-replies/${review.id}`, {
                reply,
              });

              await loadData();
            }}
          >
            Reply
          </Button>
        )}
          </Box>
        ))}
      </Paper>
      <Button
        variant="contained"
        sx={{ mt: 3 }}
        onClick={saveRestaurant}
        >
        Save Changes
      </Button>
    </MainLayout>
  );
}