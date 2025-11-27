import java.sql.*;
import java.util.*;

public class DBConnection {
    private Connection conn;
    private String url = "jdbc:mysql://localhost:3306/interview_system";
    private String user = "root";
    private String password = "";
    private boolean isConnected = false;
    
    public DBConnection() {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            conn = DriverManager.getConnection(url, user, password);
            isConnected = true;
            System.out.println("[DB] Connected to database");
        } catch (Exception e) {
            System.out.println("[DB] Warning: Database not available - " + e.getMessage());
            System.out.println("[DB] Continuing without database persistence");
            isConnected = false;
            conn = null;
        }
    }
    
    public void close() {
        try {
            if (conn != null && isConnected) {
                conn.close();
            }
        } catch (SQLException e) {
            System.out.println("[DB] Error closing connection: " + e.getMessage());
        }
    }
    
    // User operations
    public Map<String, Object> getUserByEmail(String email) throws SQLException {
        if (!isConnected) {
            System.out.println("[DB] Mock: getUserByEmail for " + email);
            return null;
        }
        String query = "SELECT id, name, password FROM users WHERE email = ?";
        PreparedStatement pstmt = conn.prepareStatement(query);
        pstmt.setString(1, email);
        ResultSet rs = pstmt.executeQuery();
        
        if (rs.next()) {
            Map<String, Object> user = new HashMap<>();
            user.put("id", rs.getInt("id"));
            user.put("name", rs.getString("name"));
            user.put("password", rs.getString("password"));
            return user;
        }
        return null;
    }
    
    public boolean createUser(String name, String email, String password) {
        if (!isConnected) {
            System.out.println("[DB] Mock: createUser - " + email);
            return true;
        }
        try {
            String query = "INSERT INTO users (name, email, password, created_at) VALUES (?, ?, ?, NOW())";
            PreparedStatement pstmt = conn.prepareStatement(query);
            pstmt.setString(1, name);
            pstmt.setString(2, email);
            pstmt.setString(3, password);
            pstmt.executeUpdate();
            return true;
        } catch (SQLException e) {
            return false;
        }
    }
    
    // Resume operations
    public int saveResume(int userId, String resumeText) {
        if (!isConnected) {
            System.out.println("[DB] Mock: saveResume for user " + userId);
            return 1;
        }
        try {
            String query = "INSERT INTO resumes (user_id, resume_text, uploaded_at) VALUES (?, ?, NOW())";
            PreparedStatement pstmt = conn.prepareStatement(query, Statement.RETURN_GENERATED_KEYS);
            pstmt.setInt(1, userId);
            pstmt.setString(2, resumeText);
            pstmt.executeUpdate();
            
            ResultSet rs = pstmt.getGeneratedKeys();
            if (rs.next()) {
                return rs.getInt(1);
            }
        } catch (SQLException e) {
            System.out.println("[DB] Error saving resume: " + e.getMessage());
        }
        return -1;
    }
    
    public String getSkillsByUser(int userId) {
        if (!isConnected) {
            System.out.println("[DB] Mock: getSkillsByUser for user " + userId);
            return "[\"Java\",\"Python\",\"JavaScript\"]";
        }
        try {
            String query = "SELECT GROUP_CONCAT(skill_name) as skills FROM skills WHERE user_id = ?";
            PreparedStatement pstmt = conn.prepareStatement(query);
            pstmt.setInt(1, userId);
            ResultSet rs = pstmt.executeQuery();
            
            if (rs.next()) {
                String skills = rs.getString("skills");
                return "[\"" + (skills != null ? skills.replace(",", "\",\"") : "") + "\"]";
            }
        } catch (SQLException e) {
            System.out.println("[DB] Error getting skills: " + e.getMessage());
        }
        return "[]";
    }
    
    // Skills operations
    public void saveSkills(int userId, int resumeId, String[] skills) {
        if (!isConnected) {
            System.out.println("[DB] Mock: saveSkills for user " + userId);
            return;
        }
        try {
            String query = "INSERT INTO skills (user_id, resume_id, skill_name, created_at) VALUES (?, ?, ?, NOW())";
            PreparedStatement pstmt = conn.prepareStatement(query);
            
            for (String skill : skills) {
                pstmt.setInt(1, userId);
                pstmt.setInt(2, resumeId);
                pstmt.setString(3, skill);
                pstmt.addBatch();
            }
            pstmt.executeBatch();
        } catch (SQLException e) {
            System.out.println("[DB] Error saving skills: " + e.getMessage());
        }
    }
    
    // Interview session operations
    public int createInterviewSession(int userId, String skills) {
        if (!isConnected) {
            System.out.println("[DB] Mock: createInterviewSession for user " + userId);
            return 1;
        }
        try {
            String query = "INSERT INTO interview_sessions (user_id, skills, started_at, status) VALUES (?, ?, NOW(), 'in_progress')";
            PreparedStatement pstmt = conn.prepareStatement(query, Statement.RETURN_GENERATED_KEYS);
            pstmt.setInt(1, userId);
            pstmt.setString(2, skills);
            pstmt.executeUpdate();
            
            ResultSet rs = pstmt.getGeneratedKeys();
            if (rs.next()) {
                return rs.getInt(1);
            }
        } catch (SQLException e) {
            System.out.println("[DB] Error creating interview session: " + e.getMessage());
        }
        return -1;
    }
    
    // Answer operations
    public void saveAnswer(int sessionId, String question, String answer, int score, String feedback) {
        if (!isConnected) {
            System.out.println("[DB] Mock: saveAnswer - session=" + sessionId + ", score=" + score);
            return;
        }
        try {
            String query = "INSERT INTO answers (session_id, question, answer, score, feedback, answered_at) VALUES (?, ?, ?, ?, ?, NOW())";
            PreparedStatement pstmt = conn.prepareStatement(query);
            pstmt.setInt(1, sessionId);
            pstmt.setString(2, question);
            pstmt.setString(3, answer);
            pstmt.setInt(4, score);
            pstmt.setString(5, feedback);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println("[DB] Error saving answer: " + e.getMessage());
        }
    }
    
    // Progress operations
    public void saveProgress(int userId, int sessionId, int score) {
        if (!isConnected) {
            System.out.println("[DB] Mock: saveProgress - userId=" + userId + ", sessionId=" + sessionId + ", score=" + score);
            return;
        }
        try {
            String query = "INSERT INTO progress_history (user_id, session_id, final_score, completed_at) VALUES (?, ?, ?, NOW())";
            PreparedStatement pstmt = conn.prepareStatement(query);
            pstmt.setInt(1, userId);
            pstmt.setInt(2, sessionId);
            pstmt.setInt(3, score);
            pstmt.executeUpdate();
            
            // Update session status
            String updateQuery = "UPDATE interview_sessions SET status = 'completed', ended_at = NOW() WHERE id = ?";
            PreparedStatement updateStmt = conn.prepareStatement(updateQuery);
            updateStmt.setInt(1, sessionId);
            updateStmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println("[DB] Error saving progress: " + e.getMessage());
        }
    }
    
    public String getHistory(int userId) {
        if (!isConnected) {
            System.out.println("[DB] Mock: getHistory for user " + userId);
            return "[]";
        }
        try {
            String query = "SELECT ph.id, ph.session_id, ph.final_score, ph.completed_at, " +
                           "COUNT(a.id) as answer_count FROM progress_history ph " +
                           "LEFT JOIN answers a ON ph.session_id = a.session_id " +
                           "WHERE ph.user_id = ? GROUP BY ph.id ORDER BY ph.completed_at DESC";
            PreparedStatement pstmt = conn.prepareStatement(query);
            pstmt.setInt(1, userId);
            ResultSet rs = pstmt.executeQuery();
            
            StringBuilder json = new StringBuilder("[");
            boolean first = true;
            while (rs.next()) {
                if (!first) json.append(",");
                json.append("{\"id\":").append(rs.getInt("id"))
                    .append(",\"sessionId\":").append(rs.getInt("session_id"))
                    .append(",\"score\":").append(rs.getInt("final_score"))
                    .append(",\"answers\":").append(rs.getInt("answer_count"))
                    .append(",\"date\":\"").append(rs.getString("completed_at")).append("\"}");
                first = false;
            }
            json.append("]");
            return json.toString();
        } catch (SQLException e) {
            System.out.println("[DB] Error getting history: " + e.getMessage());
        }
        return "[]";
    }
}

