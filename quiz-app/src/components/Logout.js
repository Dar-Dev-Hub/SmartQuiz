// eslint-disable-next-line
import { useEffect } from "react";
import { useHistory } from "react-router-dom";
import useToken from ".token";
/**
 * Logout Component
 * @returns  Delete Token And Redirect
 */
export default function Logout() {
    let history = useHistory();
    const { token, setToken } = useToken();

    const Token = "Bearer ".concat(token);
    useEffect(() => {
        localStorage.removeItem("token");
        history.push("/login");
    }, []);
    return 0;
}