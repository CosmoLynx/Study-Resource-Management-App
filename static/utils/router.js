import Home from "../pages/Home.js"
import Login from "../pages/Login.js"
import Logout from "../pages/Logout.js"
import Signup from "../pages/Signup.js"
import Profile from "../pages/Profile.js"

const routes = [
    {path : "/",component : Home},
    {path : "/login",component : Login},
    {path : "/logout",component : Logout},
    {path : "/signup",component : Signup},
    {path : "/profile",component : Profile},
];

const router = new VueRouter({
    routes,
});

export default router;