/**
 * WARGAME FRONTEND - MINIMALIST DESIGN
 * 
 * Simple 2-column interface: Squad list on left, creation form on right.
 * Focus on squad creation only - unit management removed for simplicity.
 */

// ============================
// MAIN APPLICATION CLASS
// ============================

class WargameApp {
    constructor() {
        // Configuration
        this.apiUrl = "https://wargame-mbpq.onrender.com/api";
        
        // Start the app
        this.init();
    }

    async init() {
        console.log("🏰 Starting Wargame...");
        await this.loadSquads();
        console.log("⚔️ Wargame ready!");
    }

    // ============================
    // SQUAD MANAGEMENT
    // ============================
    
    async loadSquads() {
        /**
         * Load top 5 squads and display them in the left column
         */
        try {
            const response = await fetch(`${this.apiUrl}/squads`);
            if (response.ok) {
                const allSquads = await response.json();
                // Take only the first 5 squads
                const topSquads = allSquads.slice(0, 5);
                this.displaySquads(topSquads);
                console.log(`🏰 Loaded ${topSquads.length} squads (showing top 5)`);
            } else {
                console.error("❌ Failed to load squads");
                this.displaySquads([]);
            }
        } catch (error) {
            console.error("❌ Error loading squads:", error);
            this.displaySquads([]);
        }
    }

    displaySquads(squads) {
        /**
         * Display squads in the left column (simple list, no interactions)
         */
        const squadsList = document.getElementById('squads-list');
        squadsList.innerHTML = '';

        if (squads.length === 0) {
            // Show empty state
            const emptyMessage = document.createElement('div');
            emptyMessage.className = 'placeholder-content';
            emptyMessage.innerHTML = 'No squads yet.<br>Create the first one!';
            squadsList.appendChild(emptyMessage);
        } else {
            // Create squad boxes (display only)
            squads.forEach(squad => {
                const squadBox = document.createElement('div');
                squadBox.className = 'squad-box';
                
                const commanderText = squad.commander ? `Commander: ${squad.commander}` : 'No commander assigned';
                
                squadBox.innerHTML = `
                    <div class="squad-name">${squad.name}</div>
                    <div class="squad-commander">${commanderText}</div>
                    <div class="squad-description">${squad.description || 'No description'}</div>
                `;
                
                squadsList.appendChild(squadBox);
            });
        }
    }

    // ============================
    // FORM MANAGEMENT
    // ============================

    showCreateForm() {
        /**
         * Show the creation form, hide the create button
         */
        document.getElementById('create-button-container').style.display = 'none';
        document.getElementById('create-form-container').style.display = 'block';
        
        // Focus on the name field
        document.getElementById('squad-name').focus();
        console.log("📝 Showing create form");
    }

    hideCreateForm() {
        /**
         * Hide the creation form, show the create button, clear form
         */
        document.getElementById('create-form-container').style.display = 'none';
        document.getElementById('create-button-container').style.display = 'block';
        
        // Clear form fields
        document.getElementById('squad-name').value = '';
        document.getElementById('squad-commander').value = '';
        document.getElementById('squad-description').value = '';
        
        console.log("❌ Hiding create form");
    }

    async createSquad() {
        /**
         * Create a new squad using the form data
         */
        const name = document.getElementById('squad-name').value.trim();
        const commander = document.getElementById('squad-commander').value.trim();
        const description = document.getElementById('squad-description').value.trim();

        // Validate required fields
        if (!name) {
            alert('Squad name is required!');
            document.getElementById('squad-name').focus();
            return;
        }

        try {
            const response = await fetch(`${this.apiUrl}/squads`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: name,
                    commander: commander || '',
                    description: description || ''
                })
            });

            if (response.ok) {
                console.log(`✅ Squad created: ${name} by ${commander || 'Anonymous'}`);
                
                // Hide form and refresh the squad list
                this.hideCreateForm();
                await this.loadSquads();
                
            } else {
                const error = await response.json();
                alert(`Failed to create squad: ${error.error || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('❌ Error creating squad:', error);
            alert('Error creating squad. Please try again.');
        }
    }
}

// ============================
// GLOBAL EVENT HANDLERS
// ============================
// These functions are called by onclick attributes in the HTML

function showCreateForm() {
    app.showCreateForm();
}

function hideCreateForm() {
    app.hideCreateForm();
}

function createSquad() {
    app.createSquad();
}

// ============================
// APPLICATION INITIALIZATION
// ============================

let app; // Global app instance

document.addEventListener('DOMContentLoaded', function() {
    app = new WargameApp();
    
    // Add Enter key support for form submission
    const formInputs = document.querySelectorAll('#create-form-container input[type="text"]');
    formInputs.forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                createSquad();
            }
        });
    });
}); 