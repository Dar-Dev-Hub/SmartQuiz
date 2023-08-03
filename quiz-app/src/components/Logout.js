// eslint-disable-next-line
import { useEffect } from "react";
/**
 * Logout Component
 * @returns  Delete Token And Redirect
 */
export default function Logout() {
    useEffect(() => {
        localStorage.removeItem("token");
        localStorage.removeItem("quizSubmissionId");
        localStorage.removeItem("lastQuestionId");

        history.push("/login");
    }, []);
    return 0;
}