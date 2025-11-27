import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import java.io.*;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class MainServer {
    private static int PORT = 8080;
    private static String PYTHON_SERVICE_URL = "http://localhost:5000";
    
    // Mock in-memory storage
    static Map<String, String> users = new HashMap<>();
    static int nextUserId = 100;
    
    static {
        // Add test user
        users.put("john@example.com:password123", "1:John Doe");
    }
    
    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress("0.0.0.0", PORT), 0);
        
        // API Routes
        server.createContext("/api/login", new LoginHandler());
        server.createContext("/api/signup", new SignupHandler());
        server.createContext("/api/uploadResume", new UploadResumeHandler());
        server.createContext("/api/getSkills", new GetSkillsHandler());
        server.createContext("/api/startInterview", new StartInterviewHandler());
        server.createContext("/api/nextQuestion", new NextQuestionHandler());
        server.createContext("/api/evaluateAnswer", new EvaluateAnswerHandler());
        server.createContext("/api/saveProgress", new SaveProgressHandler());
        server.createContext("/api/history", new HistoryHandler());
        
        // Frontend routes
        server.createContext("/", new StaticFileHandler());
        
        server.setExecutor(null);
        server.start();
        System.out.println("✓ Server running on http://localhost:" + PORT);
        System.out.println("✓ Test login: john@example.com / password123");
    }
    
    // CORS helper
    static void enableCORS(HttpExchange exchange) {
        exchange.getResponseHeaders().add("Access-Control-Allow-Origin", "*");
        exchange.getResponseHeaders().add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE");
        exchange.getResponseHeaders().add("Access-Control-Allow-Headers", "Content-Type, Authorization");
    }
    
    // Static file handler
    static class StaticFileHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            enableCORS(exchange);
            if (exchange.getRequestMethod().equals("OPTIONS")) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            
            String path = exchange.getRequestURI().getPath();
            if (path.equals("/")) path = "/index.html";
            
            // Try multiple path resolutions
            String[] possiblePaths = {
                "../../frontend" + path,
                "../../../frontend" + path,
                "frontend" + path,
                new File("").getAbsolutePath() + "/../../frontend" + path
            };
            
            File file = null;
            for (String p : possiblePaths) {
                File f = new File(p);
                if (f.exists() && f.isFile()) {
                    file = f;
                    break;
                }
            }
            
            if (file != null) {
                String mimeType = getMimeType(file.getPath());
                exchange.getResponseHeaders().add("Content-Type", mimeType);
                byte[] content = readFile(file);
                exchange.sendResponseHeaders(200, content.length);
                exchange.getResponseBody().write(content);
            } else {
                String response = "404 Not Found: " + path;
                exchange.getResponseHeaders().add("Content-Type", "text/plain");
                exchange.sendResponseHeaders(404, response.length());
                exchange.getResponseBody().write(response.getBytes());
            }
            exchange.close();
        }
        
        private String getMimeType(String path) {
            if (path.endsWith(".html")) return "text/html";
            if (path.endsWith(".css")) return "text/css";
            if (path.endsWith(".js")) return "application/javascript";
            if (path.endsWith(".json")) return "application/json";
            return "text/plain";
        }
        
        private byte[] readFile(File file) throws IOException {
            FileInputStream fis = new FileInputStream(file);
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            byte[] buffer = new byte[1024];
            int length;
            while ((length = fis.read(buffer)) != -1) {
                baos.write(buffer, 0, length);
            }
            fis.close();
            return baos.toByteArray();
        }
    }
    
    // Login Handler
    static class LoginHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            enableCORS(exchange);
            if (exchange.getRequestMethod().equals("OPTIONS")) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            
            String body = readBody(exchange);
            System.out.println("[LOGIN] Request body: " + body);
            Map<String, String> params = parseJSON(body);
            System.out.println("[LOGIN] Parsed params: " + params);
            
            String email = params.get("email");
            String password = params.get("password");
            
            System.out.println("[LOGIN] Email: '" + email + "', Password: '" + password + "'");
            System.out.println("[LOGIN] Available users: " + users.keySet());
            
            try {
                if (email == null || password == null) {
                    sendJSON(exchange, 400, "{\"success\":false,\"message\":\"Missing email or password\"}");
                    exchange.close();
                    return;
                }
                
                String key = email + ":" + password;
                System.out.println("[LOGIN] Looking for key: '" + key + "'");
                
                if (users.containsKey(key)) {
                    String[] userData = users.get(key).split(":");
                    String response = "{\"success\":true,\"userId\":" + userData[0] + ",\"name\":\"" + userData[1] + "\"}";
                    System.out.println("[LOGIN] Response: " + response);
                    sendJSON(exchange, 200, response);
                } else {
                    sendJSON(exchange, 401, "{\"success\":false,\"message\":\"Invalid credentials\"}");
                }
            } catch (Exception e) {
                System.out.println("[LOGIN] Error: " + e.getMessage());
                e.printStackTrace();
                sendError(exchange, e.getMessage());
            }
            exchange.close();
        }
    }
    
    // Signup Handler
    static class SignupHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            enableCORS(exchange);
            if (exchange.getRequestMethod().equals("OPTIONS")) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            
            String body = readBody(exchange);
            Map<String, String> params = parseJSON(body);
            
            String name = params.get("name");
            String email = params.get("email");
            String password = params.get("password");
            
            try {
                String key = email + ":" + password;
                if (users.containsKey(key)) {
                    String response = "{\"success\": false, \"message\": \"User already exists\"}";
                    exchange.getResponseHeaders().add("Content-Type", "application/json");
                    exchange.sendResponseHeaders(400, response.length());
                    exchange.getResponseBody().write(response.getBytes());
                } else {
                    int newUserId = nextUserId++;
                    users.put(key, newUserId + ":" + name);
                    String response = "{\"success\": true, \"message\": \"User created\", \"userId\": " + newUserId + "}";
                    exchange.getResponseHeaders().add("Content-Type", "application/json");
                    exchange.sendResponseHeaders(200, response.length());
                    exchange.getResponseBody().write(response.getBytes());
                }
            } catch (Exception e) {
                sendError(exchange, e.getMessage());
            }
            exchange.close();
        }
    }
    
    // Upload Resume Handler
    static class UploadResumeHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            System.out.println("[UploadResume] Handler called");
            enableCORS(exchange);
            if (exchange.getRequestMethod().equals("OPTIONS")) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            
            String body = readBody(exchange);
            System.out.println("[UploadResume] Request body: " + body);
            Map<String, String> params = parseJSON(body);
            
            String userId = params.get("userId");
            String resumeText = params.get("resumeText");
            
            System.out.println("[UploadResume] userId=" + userId + ", resumeText length=" + (resumeText != null ? resumeText.length() : 0));
            
            try {
                // Call Python service to extract skills
                String pythonPayload = "{\"resume_text\": \"" + escapeJSON(resumeText) + "\"}";
                System.out.println("[UploadResume] Python payload: " + pythonPayload);
                
                String pythonResponse = callPythonService("/extract-skills", pythonPayload);
                System.out.println("[UploadResume] Python response: " + pythonResponse);
                
                // Extract skills array from Python response
                String skillsJson = "[\"General\", \"Problem Solving\"]";
                try {
                    Map<String, String> pythonData = parseJSON(pythonResponse);
                    if (pythonData.containsKey("skills")) {
                        // The skills value might be a JSON array as string, or already parsed
                        String skillsValue = pythonData.get("skills");
                        if (skillsValue.startsWith("[")) {
                            skillsJson = skillsValue;
                        } else {
                            // Parse individual skills
                            skillsJson = "[\"" + skillsValue.replace(",", "\",\"") + "\"]";
                        }
                    }
                } catch (Exception parseErr) {
                    System.out.println("[UploadResume] Failed to parse Python response: " + pythonResponse);
                }
                
                String response = "{\"success\": true, \"resumeId\": 1, \"skills\": " + skillsJson + "}";
                System.out.println("[UploadResume] Sending response: " + response);
                sendJSON(exchange, 200, response);
            } catch (Exception e) {
                System.out.println("[UploadResume] Error: " + e.getMessage());
                e.printStackTrace();
                sendError(exchange, e.getMessage());
            }
            exchange.close();
        }
    }
    
    // Get Skills Handler
    static class GetSkillsHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            enableCORS(exchange);
            if (exchange.getRequestMethod().equals("OPTIONS")) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            
            String userId = exchange.getRequestURI().getQuery().split("=")[1];
            
            try {
                DBConnection db = new DBConnection();
                String skills = db.getSkillsByUser(Integer.parseInt(userId));
                db.close();
                
                String response = "{\"success\": true, \"skills\": " + skills + "}";
                exchange.getResponseHeaders().add("Content-Type", "application/json");
                exchange.sendResponseHeaders(200, response.length());
                exchange.getResponseBody().write(response.getBytes());
            } catch (Exception e) {
                sendError(exchange, e.getMessage());
            }
            exchange.close();
        }
    }
    
    // Start Interview Handler
    static class StartInterviewHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            System.out.println("[StartInterview] Handler called");
            enableCORS(exchange);
            if (exchange.getRequestMethod().equals("OPTIONS")) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            
            String body = readBody(exchange);
            System.out.println("[StartInterview] Request body: " + body);
            Map<String, String> params = parseJSON(body);
            
            String userId = params.get("userId");
            String skills = params.get("skills");
            
            System.out.println("[StartInterview] userId=" + userId + ", skills=" + skills);
            
            try {
                // Generate first question via Python - pass skills as JSON array
                String pythonPayload = "{\"skills\": " + skills + ", \"question_count\": 0}";
                System.out.println("[StartInterview] Python payload: " + pythonPayload);
                
                String pythonResponse = callPythonService("/generate-question", pythonPayload);
                System.out.println("[StartInterview] Python response: " + pythonResponse);
                
                // Extract question string from Python response
                String question = "Tell me about your experience with the technologies in your resume";
                try {
                    Map<String, String> pythonData = parseJSON(pythonResponse);
                    System.out.println("[StartInterview] Parsed Python data: " + pythonData);
                    if (pythonData.containsKey("question")) {
                        question = pythonData.get("question");
                    }
                } catch (Exception parseErr) {
                    System.out.println("[StartInterview] Failed to parse Python response: " + pythonResponse);
                }
                
                String response = "{\"success\": true, \"sessionId\": 1, \"question\": \"" + escapeJSON(question) + "\"}";
                System.out.println("[StartInterview] Sending response: " + response);
                sendJSON(exchange, 200, response);
            } catch (Exception e) {
                System.out.println("[StartInterview] Error: " + e.getMessage());
                e.printStackTrace();
                sendError(exchange, e.getMessage());
            }
            exchange.close();
        }
    }
    
    // Next Question Handler
    static class NextQuestionHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            System.out.println("[NextQuestion] Handler called");
            enableCORS(exchange);
            if (exchange.getRequestMethod().equals("OPTIONS")) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            
            String body = readBody(exchange);
            System.out.println("[NextQuestion] Request body: " + body);
            Map<String, String> params = parseJSON(body);
            System.out.println("[NextQuestion] Parsed params: " + params);
            
            String sessionId = params.get("sessionId");
            String skills = params.get("skills");
            String questionCount = params.get("questionCount");
            
            System.out.println("[NextQuestion] sessionId=" + sessionId + ", skills=" + skills + ", questionCount=" + questionCount);
            
            try {
                // Generate next question via Python - pass skills as JSON array
                String pythonPayload = "{\"skills\": " + skills + ", \"question_count\": " + questionCount + "}";
                System.out.println("[NextQuestion] Python payload: " + pythonPayload);
                
                String pythonResponse = callPythonService("/generate-question", pythonPayload);
                System.out.println("[NextQuestion] Python response: " + pythonResponse);
                
                // Extract question string from Python response using proper JSON parsing
                String question = "What is your experience with the technologies you listed?";
                try {
                    Map<String, String> pythonData = parseJSON(pythonResponse);
                    System.out.println("[NextQuestion] Parsed Python data: " + pythonData);
                    if (pythonData.containsKey("question")) {
                        question = pythonData.get("question");
                    }
                } catch (Exception parseErr) {
                    System.out.println("[NextQuestion] Failed to parse Python response: " + pythonResponse);
                    parseErr.printStackTrace();
                }
                
                String response = "{\"success\":true,\"question\":\"" + escapeJSON(question) + "\"}"; 
                System.out.println("[NextQuestion] Sending response: " + response);
                sendJSON(exchange, 200, response);
            } catch (Exception e) {
                System.out.println("[NextQuestion] Error: " + e.getMessage());
                e.printStackTrace();
                sendError(exchange, e.getMessage());
            }
            exchange.close();
        }
    }
    
    // Evaluate Answer Handler
    static class EvaluateAnswerHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            System.out.println("[EvaluateAnswer] Handler called");
            enableCORS(exchange);
            if (exchange.getRequestMethod().equals("OPTIONS")) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            
            String body = readBody(exchange);
            System.out.println("[EvaluateAnswer] Request body: " + body);
            Map<String, String> params = parseJSON(body);
            System.out.println("[EvaluateAnswer] Parsed params: " + params);
            
            String sessionId = params.get("sessionId");
            String question = params.get("question");
            String answer = params.get("answer");
            
            System.out.println("[EvaluateAnswer] sessionId=" + sessionId + ", question=" + (question != null ? question.substring(0, Math.min(50, question.length())) : "null"));
            
            try {
                // Score answer via Python
                String pythonPayload = "{\"question\": \"" + escapeJSON(question) + "\", \"answer\": \"" + escapeJSON(answer) + "\"}";
                System.out.println("[EvaluateAnswer] Calling Python with payload length: " + pythonPayload.length());
                
                String scoreJson = callPythonService("/evaluate-answer", pythonPayload);
                System.out.println("[EvaluateAnswer] Python response: " + scoreJson);
                
                // Extract score and feedback from Python response using proper JSON parsing
                int score = 50;
                String feedback = "Good response";
                
                try {
                    Map<String, String> pythonData = parseJSON(scoreJson);
                    System.out.println("[EvaluateAnswer] Parsed Python data: " + pythonData);
                    if (pythonData.containsKey("score")) {
                        try {
                            score = Integer.parseInt(pythonData.get("score"));
                        } catch (NumberFormatException e) {
                            score = 50;
                        }
                    }
                    if (pythonData.containsKey("feedback")) {
                        feedback = pythonData.get("feedback");
                    }
                } catch (Exception parseErr) {
                    System.out.println("[EvaluateAnswer] Failed to parse Python response: " + scoreJson);
                    parseErr.printStackTrace();
                }
                
                System.out.println("[EvaluateAnswer] Score=" + score + ", Feedback=" + feedback);
                System.out.println("[EvaluateAnswer] Saving to database...");
                
                try {
                    DBConnection db = new DBConnection();
                    db.saveAnswer(Integer.parseInt(sessionId), question, answer, score, feedback);
                    db.close();
                    System.out.println("[EvaluateAnswer] Saved to database");
                } catch (Exception dbErr) {
                    System.out.println("[EvaluateAnswer] Database error: " + dbErr.getMessage());
                    dbErr.printStackTrace();
                    // Continue anyway, don't fail
                }
                
                String response = "{\"success\":true,\"score\":" + score + ",\"feedback\":\"" + escapeJSON(feedback) + "\"}";
                System.out.println("[EvaluateAnswer] Sending response: " + response);
                sendJSON(exchange, 200, response);
            } catch (Exception e) {
                System.out.println("[EvaluateAnswer] Error: " + e.getMessage());
                e.printStackTrace();
                sendError(exchange, e.getMessage());
            }
            exchange.close();
        }
    }
    
    // Save Progress Handler
    static class SaveProgressHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            System.out.println("[SaveProgress] Handler called");
            enableCORS(exchange);
            if (exchange.getRequestMethod().equals("OPTIONS")) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            
            String body = readBody(exchange);
            System.out.println("[SaveProgress] Request body: " + body);
            Map<String, String> params = parseJSON(body);
            System.out.println("[SaveProgress] Parsed params: " + params);
            
            String userId = params.get("userId");
            String sessionId = params.get("sessionId");
            String score = params.get("score");
            
            System.out.println("[SaveProgress] userId=" + userId + ", sessionId=" + sessionId + ", score=" + score);
            
            try {
                System.out.println("[SaveProgress] Connecting to database...");
                DBConnection db = new DBConnection();
                db.saveProgress(Integer.parseInt(userId), Integer.parseInt(sessionId), Integer.parseInt(score));
                db.close();
                System.out.println("[SaveProgress] Saved to database");
                
                String response = "{\"success\":true,\"message\":\"Progress saved\"}";
                System.out.println("[SaveProgress] Sending response: " + response);
                sendJSON(exchange, 200, response);
            } catch (Exception e) {
                System.out.println("[SaveProgress] Error: " + e.getMessage());
                e.printStackTrace();
                sendError(exchange, e.getMessage());
            }
            exchange.close();
        }
    }
    
    // History Handler
    static class HistoryHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            enableCORS(exchange);
            if (exchange.getRequestMethod().equals("OPTIONS")) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            
            String userId = exchange.getRequestURI().getQuery().split("=")[1];
            
            try {
                DBConnection db = new DBConnection();
                String history = db.getHistory(Integer.parseInt(userId));
                db.close();
                
                String response = "{\"success\": true, \"history\": " + history + "}";
                exchange.getResponseHeaders().add("Content-Type", "application/json");
                exchange.sendResponseHeaders(200, response.length());
                exchange.getResponseBody().write(response.getBytes());
            } catch (Exception e) {
                sendError(exchange, e.getMessage());
            }
            exchange.close();
        }
    }
    
    // Utility methods
    static String readBody(HttpExchange exchange) throws IOException {
        InputStream is = exchange.getRequestBody();
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        byte[] buffer = new byte[1024];
        int length;
        while ((length = is.read(buffer)) != -1) {
            baos.write(buffer, 0, length);
        }
        return baos.toString();
    }
    
    static Map<String, String> parseJSON(String json) {
        Map<String, String> map = new HashMap<>();
        try {
            // Remove outer braces
            json = json.trim();
            if (json.startsWith("{")) json = json.substring(1);
            if (json.endsWith("}")) json = json.substring(0, json.length() - 1);
            
            // Split by comma (careful with nested content - handle quotes, brackets, and braces)
            int quoteDepth = 0;
            int bracketDepth = 0;
            int braceDepth = 0;
            StringBuilder current = new StringBuilder();
            for (char c : json.toCharArray()) {
                if (c == '"' && (current.length() == 0 || current.charAt(current.length() - 1) != '\\')) {
                    quoteDepth = (quoteDepth == 0) ? 1 : 0;
                }
                if (c == '[' && quoteDepth == 0) bracketDepth++;
                if (c == ']' && quoteDepth == 0) bracketDepth--;
                if (c == '{' && quoteDepth == 0) braceDepth++;
                if (c == '}' && quoteDepth == 0) braceDepth--;
                
                if (c == ',' && quoteDepth == 0 && bracketDepth == 0 && braceDepth == 0) {
                    parsePair(current.toString(), map);
                    current = new StringBuilder();
                } else {
                    current.append(c);
                }
            }
            if (current.length() > 0) {
                parsePair(current.toString(), map);
            }
        } catch (Exception e) {
            System.out.println("JSON parse error: " + e.getMessage());
        }
        return map;
    }
    
    static void parsePair(String pair, Map<String, String> map) {
        pair = pair.trim();
        int colonIndex = pair.indexOf(":");
        if (colonIndex > 0) {
            String key = pair.substring(0, colonIndex).trim().replace("\"", "");
            String value = pair.substring(colonIndex + 1).trim();
            
            // For arrays and objects, keep them as-is (don't strip quotes inside them)
            if (value.startsWith("[") && value.endsWith("]")) {
                // Keep array intact with all quotes
                map.put(key, value);
                System.out.println("Parsed: key='" + key + "', value='" + value + "' (ARRAY)");
            } else if (value.startsWith("{") && value.endsWith("}")) {
                // Keep object intact
                map.put(key, value);
                System.out.println("Parsed: key='" + key + "', value='" + value + "' (OBJECT)");
            } else {
                // For regular strings, remove surrounding quotes
                if (value.startsWith("\"") && value.endsWith("\"")) {
                    value = value.substring(1, value.length() - 1);
                }
                map.put(key, value);
                System.out.println("Parsed: key='" + key + "', value='" + value + "'");
            }
        }
    }
    
    static String escapeJSON(String str) {
        if (str == null) return "";
        return str.replace("\\", "\\\\")
                  .replace("\"", "\\\"")
                  .replace("\n", "\\n")
                  .replace("\r", "\\r");
    }
    
    static String callPythonService(String endpoint, String payload) throws Exception {
        try {
            java.net.URL url = new java.net.URL(PYTHON_SERVICE_URL + endpoint);
            java.net.HttpURLConnection conn = (java.net.HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setDoOutput(true);
            conn.setConnectTimeout(5000);
            conn.setReadTimeout(5000);
            
            OutputStream os = conn.getOutputStream();
            os.write(payload.getBytes(StandardCharsets.UTF_8));
            os.flush();
            os.close();
            
            BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8));
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
                response.append(line);
            }
            br.close();
            return response.toString();
        } catch (Exception e) {
            System.out.println("Python service error: " + e.getMessage());
            return "{\"skills\": [\"General\"], \"question\": \"Tell me about yourself\", \"score\": 75, \"feedback\": \"Good response\"}";
        }
    }
    
    static void sendError(HttpExchange exchange, String message) throws IOException {
        String response = "{\"success\":false,\"error\":\"" + escapeJSON(message) + "\"}";
        byte[] bytes = response.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().add("Content-Type", "application/json");
        exchange.sendResponseHeaders(500, bytes.length);
        exchange.getResponseBody().write(bytes);
        exchange.getResponseBody().flush();
    }
    
    static void sendJSON(HttpExchange exchange, int status, String response) throws IOException {
        byte[] bytes = response.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().add("Content-Type", "application/json");
        exchange.sendResponseHeaders(status, bytes.length);
        exchange.getResponseBody().write(bytes);
        exchange.getResponseBody().flush();
    }
}
