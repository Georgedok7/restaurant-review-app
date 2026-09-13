import { Card, CardContent, Typography, Button, Box } from "@mui/material";
import { Link } from "react-router-dom";

type Props = {
  restaurant: {
    id: number;
    name: string;
    address: string;
    category_name: string;
    average_rating: number;
    total_reviews: number;
  };
};

export default function RestaurantCard({ restaurant }: Props) {
  return (
    <Card sx={{ height: "100%", borderRadius: 3 }}>
      <CardContent>
        <Typography variant="h6" sx={{ fontWeight: 700 }}>
          {restaurant.name}
        </Typography>

        <Typography color="text.secondary">
          {restaurant.category_name}
        </Typography>

        <Typography sx={{ mt: 1 }}>
          📍 {restaurant.address}
        </Typography>

        <Typography sx={{ mt: 1 }}>
          ⭐ {restaurant.average_rating} ({restaurant.total_reviews} reviews)
        </Typography>

        <Box sx={{ mt: 2 }}>
          <Button
            component={Link}
            to={`/restaurants/${restaurant.id}`}
            variant="contained"
            fullWidth
          >
            View Details
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
}