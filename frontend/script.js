// Medieval Wargame JavaScript
class WargameAPI {
    constructor() {
        this.apiUrl = "https://wargame-mbpq.onrender.com/api"; // Replace with your API URL
        this.output = document.getElementById("output");
    }

    // Display results in the output scroll
    displayResult(data, isError = false) {
        const timestamp = new Date().toLocaleTimeString();
        let message = "";
        
        if (isError) {
            message = `⚠️ [${timestamp}] ERROR: ${data}\n\n`;
        } else {
            message = `✅ [${timestamp}] SUCCESS:\n${JSON.stringify(data, null, 2)}\n\n`;
        }
        
        this.output.textContent = message + this.output.textContent;
        
        // Scroll effect
        this.output.scrollTop = 0;
    }

    // Show loading state
    showLoading(action) {
        this.output.textContent = `⏳ ${action}...\n\n` + this.output.textContent;
    }

    // Clear form fields
    clearForm(formId) {
        const form = document.getElementById(formId);
        const inputs = form.querySelectorAll('input');
        inputs.forEach(input => input.value = '');
    }

    // Create a new user
    async createUser() {
        const username = document.getElementById("username").value.trim();
        const email = document.getElementById("email").value.trim();
        
        if (!username || !email) {
            this.displayResult("Username and email are required!", true);
            return;
        }

        this.showLoading("Creating warrior");
        
        try {
            const response = await fetch(`${this.apiUrl}/users`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, email })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.displayResult({
                    message: `🏰 Warrior "${username}" has joined the realm!`,
                    data: data
                });
                this.clearForm("user-form");
                
                // Auto-fill user ID in squad form if available
                const userIdField = document.getElementById("userId");
                if (userIdField && data.id) {
                    userIdField.value = data.id;
                }
            } else {
                this.displayResult(data.error || "Failed to create warrior", true);
            }
        } catch (error) {
            this.displayResult(`Network error: ${error.message}`, true);
        }
    }

    // Create a squad
    async createSquad() {
        const userId = document.getElementById("userId").value.trim();
        const squadName = document.getElementById("squadName").value.trim();
        const description = document.getElementById("description").value.trim() || "A mighty squad ready for battle";
        
        if (!userId || !squadName) {
            this.displayResult("User ID and squad name are required!", true);
            return;
        }

        this.showLoading("Assembling squad");
        
        try {
            const response = await fetch(`${this.apiUrl}/squads`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ 
                    user_id: parseInt(userId), 
                    name: squadName, 
                    description 
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.displayResult({
                    message: `⚔️ Squad "${squadName}" has been assembled!`,
                    data: data
                });
                this.clearForm("squad-form");
            } else {
                this.displayResult(data.error || "Failed to create squad", true);
            }
        } catch (error) {
            this.displayResult(`Network error: ${error.message}`, true);
        }
    }

    // List squads for a user
    async listSquads() {
        const userId = document.getElementById("listUserId").value.trim();
        
        if (!userId) {
            this.displayResult("User ID is required!", true);
            return;
        }

        this.showLoading("Gathering squad information");
        
        try {
            const response = await fetch(`${this.apiUrl}/users/${userId}/squads`, {
                method: "GET"
            });
            
            const data = await response.json();
            
            if (response.ok) {
                if (data.length === 0) {
                    this.displayResult({
                        message: `🏰 No squads found for warrior ${userId}`,
                        data: []
                    });
                } else {
                    this.displayResult({
                        message: `🛡️ Found ${data.length} squad(s) for warrior ${userId}:`,
                        data: data
                    });
                }
                this.clearForm("list-form");
            } else {
                this.displayResult(data.error || "Failed to retrieve squads", true);
            }
        } catch (error) {
            this.displayResult(`Network error: ${error.message}`, true);
        }
    }

    // Clear output
    clearOutput() {
        this.output.textContent = "📜 Battle logs cleared...\n\n";
    }
}

// Initialize the API when the page loads
let wargame;

document.addEventListener('DOMContentLoaded', function() {
    wargame = new WargameAPI();
    
    // Add event listeners
    document.getElementById('create-user-btn').addEventListener('click', () => wargame.createUser());
    document.getElementById('create-squad-btn').addEventListener('click', () => wargame.createSquad());
    document.getElementById('list-squads-btn').addEventListener('click', () => wargame.listSquads());
    document.getElementById('clear-output-btn').addEventListener('click', () => wargame.clearOutput());
    
    // Add Enter key support for forms
    document.getElementById('user-form').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            wargame.createUser();
        }
    });
    
    document.getElementById('squad-form').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            wargame.createSquad();
        }
    });
    
    document.getElementById('list-form').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            wargame.listSquads();
        }
    });
    
    // Welcome message
    setTimeout(() => {
        wargame.displayResult({
            message: "🏰 Welcome to the Medieval Wargame! Begin by creating a warrior...",
            tip: "Press Enter in any form to submit, or click the buttons."
        });
    }, 500);
}); 