import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  Typography,
  Box,
  Paper,
  CircularProgress,
  Button,
  Rating,
  Divider,
  TextField,
  Alert
} from "@mui/material";

import MainLayout from "../layouts/MainLayout";
import api from "../api/api";

export default function RestaurantDetails() {
  const { id } = useParams();

  const [restaurant, setRestaurant] = useState<any>(null);
  const [images, setImages] = useState<any[]>([]);
  const [reviews, setReviews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isFavorite, setIsFavorite] = useState(false);
  const [newRating, setNewRating] = useState<number | null>(5);
  const [newComment, setNewComment] = useState("");
  const [reviewMessage, setReviewMessage] = useState("");

useEffect(() => {
  async function loadData() {
    try {
      const restaurantRes = await api.get(`/restaurants/${id}`);
      const imagesRes = await api.get(`/restaurants/${id}/images`);
      const reviewsRes = await api.get(`/reviews/restaurant/${id}`);

      setRestaurant(restaurantRes.data);
      setImages(imagesRes.data);
      setReviews(reviewsRes.data);

      try {
        const favoritesRes = await api.get("/favorites");

        setIsFavorite(
          favoritesRes.data.some(
            (favorite: any) => favorite.restaurant_id === Number(id)
          )
        );
      } catch {
        setIsFavorite(false);
      }
    } finally {
      setLoading(false);
    }
  }

  loadData();
}, [id]);

  if (loading) {
    return (
      <MainLayout>
        <CircularProgress />
      </MainLayout>
    );
  }

  if (!restaurant) {
    return (
      <MainLayout>
        <Typography>Restaurant not found.</Typography>
      </MainLayout>
    );
  }
  async function addFavorite() {
    await api.post(`/favorites/${restaurant.id}`);
    setIsFavorite(true);
    }

  async function removeFavorite() {
    await api.delete(`/favorites/${restaurant.id}`);
    setIsFavorite(false);
    }
    async function submitReview() {
    if (!newRating || !newComment.trim()) return;

    try {
        await api.post(`/reviews/restaurant/${restaurant.id}`, {
        rating: newRating,
        comment: newComment,
        });

        const reviewsRes = await api.get(`/reviews/restaurant/${id}`);
        setReviews(reviewsRes.data);

        setNewRating(5);
        setNewComment("");
        setReviewMessage("Review submitted successfully!");
    } catch {
        setReviewMessage("You have already reviewed this restaurant.");
    }
    }
  return (
    <MainLayout>
      <Paper sx={{ p: 4, mb: 4, borderRadius: 3 }}>
        {images.length > 0 && (
          <Box
            component="img"
            src={images[0].image_url}
            alt={restaurant.name}
            sx={{
              width: "100%",
              height: 300,
              objectFit: "cover",
              borderRadius: 3,
              mb: 3,
            }}
          />
        )}

        <Typography variant="h3" sx={{ fontWeight: 700 }}>
          {restaurant.name}
        </Typography>

        <Typography color="text.secondary">
          {restaurant.category_name}
        </Typography>

        <Typography sx={{ mt: 2 }}>📍 {restaurant.address}</Typography>

        <Box sx={{ display: "flex", alignItems: "center", gap: 1, mt: 2 }}>
          <Rating value={restaurant.average_rating} readOnly precision={0.5} />
          <Typography>
            {restaurant.average_rating} ({restaurant.total_reviews} reviews)
          </Typography>
        </Box>

        <Typography sx={{ mt: 3 }}>{restaurant.description}</Typography>

        <Typography sx={{ mt: 2 }}>
          ☎ {restaurant.phone} | 🕒 {restaurant.opening_hours}
        </Typography>

        {isFavorite ? (
        <Button
            color="error"
            variant="contained"
            sx={{ mt: 3 }}
            onClick={removeFavorite}
        >
            ❤️ Remove from Favorites
        </Button>
        ) : (
        <Button
            variant="contained"
            sx={{ mt: 3 }}
            onClick={addFavorite}
        >
            🤍 Add to Favorites
        </Button>
        )}
      </Paper>

      <Typography variant="h5" sx={{ fontWeight: 700, mb: 2 }}>
        Reviews
      </Typography>

      {reviews.length === 0 && (
        <Typography color="text.secondary">No reviews yet.</Typography>
      )}

      {reviews.map((review) => (
        <Paper key={review.id} sx={{ p: 3, mb: 2, borderRadius: 3 }}>
          <Rating value={review.rating} readOnly />

          <Typography sx={{ mt: 1 }}>{review.comment}</Typography>
                <Button
                color="warning"
                variant="outlined"
                sx={{ mt: 2 }}
                onClick={async () => {
                    const reason = prompt("Why are you reporting this review?");

                    if (!reason) return;

                    await api.post(`/reports/review/${review.id}`, {
                    reason,
                    });

                    alert("Report submitted.");
                }}
                >
                Report Review
                </Button>

          {review.reply && (
            <>
              <Divider sx={{ my: 2 }} />
              <Typography sx={{ fontWeight: 700 }}>
                Owner Reply
              </Typography>
              <Typography color="text.secondary">
                {review.reply.reply}
              </Typography>

            </>
          )}
        </Paper>
      ))}
      <Paper sx={{ p: 3, mt: 4, borderRadius: 3 }}>
        <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
            Write a Review
        </Typography>

        {reviewMessage && (
            <Alert severity="success" sx={{ mb: 2 }}>
            {reviewMessage}
            </Alert>
        )}

        <Rating
            value={newRating}
            onChange={(_, value) => setNewRating(value)}
            sx={{ mb: 2 }}
        />

        <TextField
            label="Your comment"
            multiline
            rows={4}
            fullWidth
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            sx={{ mb: 2 }}
        />

        <Button variant="contained" onClick={submitReview}>
            Submit Review
        </Button>
        </Paper>
    </MainLayout>
  );
}