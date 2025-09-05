/**
 * WARGAME FRONTEND - MINIMALIST DESIGN
 * 
 * Simple 2-column interface: Squad list on left, creation form on right.
 * Focus on squad creation with integrated unit creation.
 */

// ============================
// MAIN APPLICATION CLASS
// ============================

class WargameApp {
    constructor() {
        // Configuration
        this.apiUrl = "https://wargame-mbpq.onrender.com/api";
        
        // State tracking
        this.gameData = {}; // Cache for races, classes, armors, weapons
        this.unitCounter = 0; // For unique unit IDs in the form
        
        // Start the app
        this.init();
    }

    async init() {
        console.log("Starting Wargame...");
        await this.loadGameData();
        await this.loadSquads();
        console.log("Wargame ready!");
    }

    // ============================
    // GAME DATA MANAGEMENT
    // ============================
    
    async loadGameData() {
        /**
         * Load dropdown options for unit creation (races, classes, armors, weapons)
         * Falls back to hardcoded data if API endpoints aren't available
         */
        try {
            // Try to load from API
            const [races, classes, armors, weapons] = await Promise.all([
                fetch(`${this.apiUrl}/races`).then(r => r.json()),
                fetch(`${this.apiUrl}/classes`).then(r => r.json()),
                fetch(`${this.apiUrl}/armors`).then(r => r.json()),
                fetch(`${this.apiUrl}/weapons`).then(r => r.json())
            ]);
            
            this.gameData = { races, classes, armors, weapons };
            console.log("Game data loaded from API");
            
        } catch (error) {
            // Use fallback data if API isn't available
            console.log("Using fallback game data");
            this.gameData = {
                races: [
                    { name: 'Man' }, { name: 'Elf' }, { name: 'Dwarf' }, { name: 'Goblin' }
                ],
                classes: [
                    { name: 'Basic' }, { name: 'Berzerker' }, { name: 'Rogue' }, 
                    { name: 'Battlemage' }, { name: 'Auramancer' }, { name: 'Healing Mage' }, 
                    { name: 'Commander' }, { name: 'Hero' }
                ],
                armors: [
                    { name: 'None' }, { name: 'Light' }, { name: 'Medium' }, { name: 'Heavy' }
                ],
                weapons: [
                    { name: 'None' }, { name: 'Infantry Sword' }, { name: 'Bow' }, { name: 'Longbow' }
                ]
            };
        }
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
                console.log(`Loaded ${topSquads.length} squads (showing top 5)`);
            } else {
                console.error("Failed to load squads");
                this.displaySquads([]);
            }
        } catch (error) {
            console.error("Error loading squads:", error);
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
        
        // Reset unit counter
        this.unitCounter = 0;
        
        // Focus on the name field
        document.getElementById('squad-name').focus();
        console.log("Showing create form");
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
        
        // Clear units
        document.getElementById('units-container').innerHTML = '';
        this.unitCounter = 0;
        
        console.log("Hiding create form");
    }

    // ============================
    // UNIT FORM MANAGEMENT
    // ============================

    addUnitForm() {
        /**
         * Add a new unit form to the units container
         */
        this.unitCounter++;
        const unitId = `unit-${this.unitCounter}`;
        
        const unitsContainer = document.getElementById('units-container');
        
        const unitForm = document.createElement('div');
        unitForm.className = 'unit-form';
        unitForm.id = unitId;
        
        unitForm.innerHTML = `
            <div class="unit-form-header">
                <span class="unit-form-title">Unit ${this.unitCounter}</span>
                <button type="button" class="remove-unit-btn" onclick="removeUnitForm('${unitId}')">×</button>
            </div>
            
            <div class="unit-name-field">
                <label for="${unitId}-name">Unit Name:</label>
                <input type="text" id="${unitId}-name" placeholder="Enter unit name...">
            </div>
            
            <div class="unit-attributes-grid">
                <div class="attribute-group">
                    <label for="${unitId}-race">Race:</label>
                    <select id="${unitId}-race">
                        <option value="">Select Race</option>
                        ${this.generateOptions(this.gameData.races)}
                    </select>
                </div>
                
                <div class="attribute-group">
                    <label for="${unitId}-class">Class:</label>
                    <select id="${unitId}-class">
                        <option value="">Select Class</option>
                        ${this.generateOptions(this.gameData.classes)}
                    </select>
                </div>
                
                <div class="attribute-group">
                    <label for="${unitId}-armor">Armor:</label>
                    <select id="${unitId}-armor">
                        <option value="">Select Armor</option>
                        ${this.generateOptions(this.gameData.armors)}
                    </select>
                </div>
                
                <div class="attribute-group">
                    <label for="${unitId}-weapon">Weapon:</label>
                    <select id="${unitId}-weapon">
                        <option value="">Select Weapon</option>
                        ${this.generateOptions(this.gameData.weapons)}
                    </select>
                </div>
            </div>
        `;
        
        unitsContainer.appendChild(unitForm);
        console.log(`Added unit form ${this.unitCounter}`);
    }

    generateOptions(items) {
        /**
         * Generate HTML option elements for dropdowns
         */
        return items.map(item => 
            `<option value="${item.name}">${item.name}</option>`
        ).join('');
    }

    // ============================
    // SQUAD + UNITS CREATION
    // ============================

    async createSquad() {
        /**
         * Create a new squad with its units
         */
        // Get squad data
        const squadName = document.getElementById('squad-name').value.trim();
        const commander = document.getElementById('squad-commander').value.trim();
        const description = document.getElementById('squad-description').value.trim();

        // Validate required fields
        if (!squadName) {
            alert('Squad name is required!');
            document.getElementById('squad-name').focus();
            return;
        }

        // Get units data
        const units = this.collectUnitsData();

        try {
            // First, create the squad
            const squadResponse = await fetch(`${this.apiUrl}/squads`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: squadName,
                    commander: commander || '',
                    description: description || ''
                })
            });

            if (!squadResponse.ok) {
                const error = await squadResponse.json();
                alert(`Failed to create squad: ${error.error || 'Unknown error'}`);
                return;
            }

            const createdSquad = await squadResponse.json();
            console.log(`Squad created: ${squadName} (ID: ${createdSquad.id})`);

            // Then, create each unit for the squad
            for (const unit of units) {
                try {
                    const unitResponse = await fetch(`${this.apiUrl}/units`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            squad_id: createdSquad.id,
                            name: unit.name,
                            race: unit.race || null,
                            class: unit.class || 'Basic',
                            level: 1,
                            armor: unit.armor || null,
                            weapon: unit.weapon || null
                        })
                    });

                    if (unitResponse.ok) {
                        console.log(`Unit created: ${unit.name}`);
                    } else {
                        console.error(`Failed to create unit: ${unit.name}`);
                    }
                } catch (error) {
                    console.error(`Error creating unit ${unit.name}:`, error);
                }
            }

            // Success - hide form and refresh list
            this.hideCreateForm();
            await this.loadSquads();
            
        } catch (error) {
            console.error('Error creating squad:', error);
            alert('Error creating squad. Please try again.');
        }
    }

    collectUnitsData() {
        /**
         * Collect data from all unit forms
         */
        const units = [];
        const unitForms = document.querySelectorAll('.unit-form');
        
        unitForms.forEach(form => {
            const unitId = form.id;
            const name = document.getElementById(`${unitId}-name`).value.trim();
            
            // Only include units with names
            if (name) {
                units.push({
                    name: name,
                    race: document.getElementById(`${unitId}-race`).value,
                    class: document.getElementById(`${unitId}-class`).value,
                    armor: document.getElementById(`${unitId}-armor`).value,
                    weapon: document.getElementById(`${unitId}-weapon`).value
                });
            }
        });
        
        return units;
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

function addUnitForm() {
    app.addUnitForm();
}

function removeUnitForm(unitId) {
    const unitForm = document.getElementById(unitId);
    if (unitForm) {
        unitForm.remove();
        console.log(`Removed unit form ${unitId}`);
    }
}

// ============================
// APPLICATION INITIALIZATION
// ============================

let app; // Global app instance

document.addEventListener('DOMContentLoaded', function() {
    app = new WargameApp();
    
    // Add Enter key support for form submission
    document.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && document.getElementById('create-form-container').style.display !== 'none') {
            e.preventDefault();
            createSquad();
        }
    });
}); 