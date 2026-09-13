import { useEffect, useState } from "react";
import {
  Box,
  Button,
  Paper,
  TextField,
  Typography,
} from "@mui/material";

import MainLayout from "../layouts/MainLayout";
import api from "../api/api";

export default function AdminCategories() {
  const [categories, setCategories] = useState<any[]>([]);
  const [newCategory, setNewCategory] = useState("");

  async function loadCategories() {
    const response = await api.get("/categories");
    setCategories(response.data);
  }

  useEffect(() => {
    loadCategories();
  }, []);

  async function addCategory() {
    if (!newCategory.trim()) return;

    await api.post("/categories", {
      name: newCategory,
    });

    setNewCategory("");

    loadCategories();
  }

  async function editCategory(category: any) {
    const name = prompt("New category name", category.name);

    if (!name) return;

    await api.put(`/categories/${category.id}`, {
      name,
    });

    loadCategories();
  }

  async function removeCategory(id: number) {
    if (!window.confirm("Delete this category?")) return;

    await api.delete(`/categories/${id}`);

    loadCategories();
  }

  return (
    <MainLayout>
      <Typography
        variant="h4"
        sx={{ fontWeight: 700, mb: 4 }}
      >
        Category Management
      </Typography>

      <Paper sx={{ p: 3, mb: 4 }}>
        <Box sx={{ display: "flex", gap: 2 }}>
          <TextField
            fullWidth
            label="New Category"
            value={newCategory}
            onChange={(e) => setNewCategory(e.target.value)}
          />

          <Button
            variant="contained"
            onClick={addCategory}
          >
            Add
          </Button>
        </Box>
      </Paper>

      {categories.map((category) => (
        <Paper
          key={category.id}
          sx={{
            p: 3,
            mb: 2,
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <Typography variant="h6">
            {category.name}
          </Typography>

          <Box sx={{ display: "flex", gap: 2 }}>
            <Button
              variant="contained"
              onClick={() => editCategory(category)}
            >
              Edit
            </Button>

            <Button
              color="error"
              variant="contained"
              onClick={() => removeCategory(category.id)}
            >
              Delete
            </Button>
          </Box>
        </Paper>
      ))}
    </MainLayout>
  );
}