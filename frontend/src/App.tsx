import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Restaurants from "./pages/Restaurants";
import RestaurantDetails from "./pages/RestaurantDetails";
import Favorites from "./pages/Favorites";
import Profile from "./pages/Profile";
import OwnerDashboard from "./pages/OwnerDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import OwnerRestaurantManage from "./pages/OwnerRestaurantManage";
import AddRestaurant from "./pages/AddRestaurant";
import AdminUsers from "./pages/AdminUsers";
import AdminCategories from "./pages/AdminCategories";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />

        <Route path="/login" element={<Login />} />

        <Route path="/register" element={<Register />} />

        <Route path="/restaurants" element={<Restaurants />}/>

        <Route path="/restaurants/:id" element={<RestaurantDetails />} />

        <Route
          path="/favorites"
          element={
            <ProtectedRoute roles={["customer"]}>
              <Favorites />
            </ProtectedRoute>
          }
        />

        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />

        <Route
          path="/owner"
          element={
            <ProtectedRoute roles={["owner"]}>
              <OwnerDashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/admin"
          element={
            <ProtectedRoute roles={["admin"]}>
              <AdminDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/owner/restaurants/:id"
          element={
            <ProtectedRoute roles={["owner"]}>
              <OwnerRestaurantManage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/owner/create"
          element={
            <ProtectedRoute roles={["owner"]}>
              <AddRestaurant />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/users"
          element={
              <ProtectedRoute roles={["admin"]}>
                  <AdminUsers />
              </ProtectedRoute>
          }
        />
        <Route
          path="/admin/categories"
          element={
            <ProtectedRoute roles={["admin"]}>
              <AdminCategories />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;