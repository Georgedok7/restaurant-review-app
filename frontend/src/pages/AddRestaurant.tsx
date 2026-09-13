import {
  Paper,
  Typography,
  TextField,
  Button,
  MenuItem,
} from "@mui/material";

import { useNavigate } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import api from "../api/api";
import { useEffect, useState } from "react";

export default function AddRestaurant() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [categoryId, setCategoryId] = useState("");
  const [description, setDescription] = useState("");
  const [address, setAddress] = useState("");
  const [phone, setPhone] = useState("");
  const [openingHours, setOpeningHours] = useState("");
  const [categories, setCategories] = useState<any[]>([]);

    async function createRestaurant() {
        await api.post("/restaurants", {
            category_id: Number(categoryId),
            name,
            description,
            address,
            phone,
            opening_hours: openingHours,
        });

        navigate("/owner");
    }
  useEffect(() => {
  async function loadCategories() {
    const response = await api.get("/categories");
    setCategories(response.data);
  }

  loadCategories();
}, []);

  return (
    <MainLayout>
      <Paper sx={{ p:4, maxWidth:700, mx:"auto" }}>
        <Typography variant="h4" sx={{ mb:4 }}>
          Add Restaurant
        </Typography>

        <TextField
          label="Name"
          value={name}
          onChange={(e)=>setName(e.target.value)}
          fullWidth
          sx={{ mb:2 }}
        />

        <TextField
        select
        label="Category"
        value={categoryId}
        onChange={(e) => setCategoryId(e.target.value)}
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
          multiline
          rows={4}
          value={description}
          onChange={(e)=>setDescription(e.target.value)}
          fullWidth
          sx={{ mb:2 }}
        />

        <TextField
          label="Address"
          value={address}
          onChange={(e)=>setAddress(e.target.value)}
          fullWidth
          sx={{ mb:2 }}
        />

        <TextField
          label="Phone"
          value={phone}
          onChange={(e)=>setPhone(e.target.value)}
          fullWidth
          sx={{ mb:2 }}
        />

        <TextField
          label="Opening Hours"
          value={openingHours}
          onChange={(e)=>setOpeningHours(e.target.value)}
          fullWidth
          sx={{ mb:3 }}
        />

        <Button
          variant="contained"
          onClick={createRestaurant}
        >
          Create Restaurant
        </Button>

      </Paper>
    </MainLayout>
  );
}