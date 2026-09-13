import { AppBar, Toolbar, Typography, Button, Box } from "@mui/material";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  return (
    <AppBar position="static" color="default" elevation={1}>
      <Toolbar>
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h6" sx={{ fontWeight: 700 }}>
              Restaurant Reviews
            </Typography>

            {user && (
              <Typography variant="body2" color="text.secondary">
                Welcome, {user.first_name}
              </Typography>
            )}
          </Box>

        <Box sx={{ display: "flex", gap: 1 }}>
          <Button component={Link} to="/">
            Home
          </Button>

          <Button component={Link} to="/restaurants">
            Restaurants
              </Button>

              {!user && (
                <>
                  <Button component={Link} to="/login">
                    Login
                  </Button>

                  <Button
                    component={Link}
                    to="/register"
                    variant="contained"
                  >
                    Register
                  </Button>
                </>
              )}

              {user?.role === "customer" && (
                <>
                  <Button component={Link} to="/favorites">
                    Favorites
                  </Button>

                  <Button component={Link} to="/profile">
                    Profile
                  </Button>

                  <Button
                    color="error"
                    onClick={() => {
                      logout();
                      navigate("/");
                    }}
                  >
                    Logout
                  </Button>
                </>
              )}

              {user?.role === "owner" && (
                <>
                  <Button component={Link} to="/owner">
                    Dashboard
                  </Button>

                  <Button component={Link} to="/profile">
                    Profile
                  </Button>

                  <Button color="error" onClick={logout}>
                    Logout
                  </Button>
                </>
              )}

              {user?.role === "admin" && (
                <>
                  <Button component={Link} to="/admin">
                    Admin
                  </Button>
                  <Button
                      component={Link}
                      to="/admin/users"
                  >
                      USERS
                  </Button>
                  <Button
                    component={Link}
                    to="/admin/categories"
                  >
                    CATEGORIES
                  </Button>
                  <Button color="error" onClick={logout}>
                    Logout
                  </Button>

                </>
              )}
            </Box>
      </Toolbar>
    </AppBar>
  );
}