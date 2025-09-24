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
        this.selectedSquad = null; // Currently selected squad
        
        // Start the app
        this.init();
    }

    async init() {
        console.log("Starting Wargame...");
        
        // Show loading state immediately
        this.showLoadingState();
        
        // Load data in parallel for better performance
        // Use Promise.allSettled to handle partial failures gracefully
        const results = await Promise.allSettled([
            this.loadGameData(),
            this.loadSquads()
        ]);
        
        // Check results and handle partial failures
        const gameDataSuccess = results[0].status === 'fulfilled';
        const squadsSuccess = results[1].status === 'fulfilled';
        
        if (!gameDataSuccess) {
            console.warn("Game data failed to load, using fallback");
        }
        if (!squadsSuccess) {
            console.warn("Squads failed to load");
        }
        
        // Hide loading state
        this.hideLoadingState();
        console.log("Wargame ready!");
    }
    
    showLoadingState() {
        /**
         * Show loading skeleton while data loads
         */
        const squadsList = document.getElementById('squads-list');
        squadsList.innerHTML = `
            <div class="loading-skeleton">
                <div class="skeleton-squad"></div>
                <div class="skeleton-squad"></div>
                <div class="skeleton-squad"></div>
                <div class="skeleton-squad"></div>
                <div class="skeleton-squad"></div>
            </div>
        `;
        
        // Update counter to show loading
        this.updateSquadCounter('Loading...');
    }
    
    hideLoadingState() {
        /**
         * Hide loading skeleton
         */
        // Loading state will be replaced by actual data
    }

    // ============================
    // GAME DATA MANAGEMENT
    // ============================
    
    async loadGameData() {
        /**
         * Load dropdown options for unit creation (races, classes, armors, weapons)
         * Uses caching and falls back to hardcoded data if API endpoints aren't available
         */
        // Check cache first
        const cacheKey = 'wargame-game-data';
        const cached = localStorage.getItem(cacheKey);
        if (cached) {
            try {
                this.gameData = JSON.parse(cached);
                console.log("Game data loaded from cache");
                return;
            } catch (e) {
                // Cache corrupted, continue with API
            }
        }
        
        try {
            // Try to load from API with timeout
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
            
            const [races, classes, armors, weapons] = await Promise.all([
                fetch(`${this.apiUrl}/races`, { signal: controller.signal }).then(r => r.json()),
                fetch(`${this.apiUrl}/classes`, { signal: controller.signal }).then(r => r.json()),
                fetch(`${this.apiUrl}/armors`, { signal: controller.signal }).then(r => r.json()),
                fetch(`${this.apiUrl}/weapons`, { signal: controller.signal }).then(r => r.json())
            ]);
            
            clearTimeout(timeoutId);
            
            this.gameData = { races, classes, armors, weapons };
            
            // Cache the data for next time
            localStorage.setItem(cacheKey, JSON.stringify(this.gameData));
            console.log("Game data loaded from API and cached");
            
        } catch (error) {
            // Use fallback data if API isn't available
            console.log("Using fallback game data due to error:", error.message);
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
         * Also update the total squad counter
         */
        try {
            // Add timeout to prevent hanging
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 8000); // 8 second timeout
            
            const response = await fetch(`${this.apiUrl}/squads`, { signal: controller.signal });
            clearTimeout(timeoutId);
            
            if (response.ok) {
                const allSquads = await response.json();
                // Update the total squad counter
                this.updateSquadCounter(allSquads.length);
                // Take only the first 5 squads
                const topSquads = allSquads.slice(0, 5);
                this.displaySquads(topSquads);
                console.log(`Loaded ${topSquads.length} squads (showing top 5 of ${allSquads.length} total)`);
            } else {
                console.error("Failed to load squads");
                this.updateSquadCounter(0);
                this.displaySquads([]);
            }
        } catch (error) {
            console.error("Error loading squads:", error.message);
            this.updateSquadCounter(0);
            this.displaySquads([]);
        }
    }

    updateSquadCounter(count) {
        /**
         * Update the squad counter display
         */
        const counter = document.getElementById('squad-counter');
        if (counter) {
            counter.textContent = `Total Squads: ${count}`;
            console.log(`Updated squad counter to: Total Squads: ${count}`);
        }
    }

    displaySquads(squads) {
        /**
         * Display squads in the left column with click functionality
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
            // Create squad boxes with click functionality
            squads.forEach(squad => {
                const squadBox = document.createElement('div');
                squadBox.className = 'squad-box';
                squadBox.dataset.squadId = squad.id;
                
                const commanderText = squad.commander ? `Commander: ${squad.commander}` : 'No commander assigned';
                
                squadBox.innerHTML = `
                    <div class="squad-name" onclick="app.selectSquad(${squad.id})">${squad.name}</div>
                    <div class="squad-commander">${commanderText}</div>
                    <div class="squad-description">${squad.description || 'No description'}</div>
                `;
                
                squadsList.appendChild(squadBox);
            });
        }
    }

    async selectSquad(squadId) {
        /**
         * Select a squad and load its units
         */
        console.log(`selectSquad called with squadId: ${squadId} (type: ${typeof squadId})`);
        
        try {
            // Update visual selection
            document.querySelectorAll('.squad-box').forEach(box => {
                box.classList.remove('selected');
            });
            const selectedBox = document.querySelector(`[data-squad-id="${squadId}"]`);
            if (selectedBox) {
                selectedBox.classList.add('selected');
                console.log(`Selected squad box found and highlighted`);
            } else {
                console.error(`Could not find squad box with data-squad-id="${squadId}"`);
            }
            
            // Hide creation form and show units
            document.getElementById('create-form-container').style.display = 'none';
            document.getElementById('squad-units-container').style.display = 'block';
            
            // Load squad units
            await this.loadSquadUnits(squadId);
            
            this.selectedSquad = squadId;
            console.log(`Selected squad: ${squadId}`);
            
        } catch (error) {
            console.error('Error selecting squad:', error);
        }
    }

    async loadSquadUnits(squadId) {
        /**
         * Load and display units for the selected squad
         */
        console.log(`Loading units for squad ID: ${squadId}`);
        
        try {
            const url = `${this.apiUrl}/squads/${squadId}/units`;
            console.log(`Fetching from URL: ${url}`);
            
            const response = await fetch(url);
            console.log(`Response status: ${response.status}`);
            console.log(`Response ok: ${response.ok}`);
            
            if (response.ok) {
                const units = await response.json();
                console.log(`Raw units data:`, units);
                console.log(`Units array length: ${units.length}`);
                
                this.displaySquadUnits(units);
                console.log(`Loaded ${units.length} units for squad ${squadId}`);
            } else {
                const errorText = await response.text();
                console.error(`Failed to load squad units. Status: ${response.status}, Error: ${errorText}`);
                this.displaySquadUnits([]);
            }
        } catch (error) {
            console.error("Error loading squad units:", error);
            this.displaySquadUnits([]);
        }
    }

    displaySquadUnits(units) {
        /**
         * Display units for the selected squad
         */
        console.log(`Displaying ${units.length} units`);
        console.log('Units data:', units);
        
        const unitsList = document.getElementById('squad-units-list');
        if (!unitsList) {
            console.error('Could not find #squad-units-list element');
            return;
        }
        
        unitsList.innerHTML = '';

        if (!units || units.length === 0) {
            // Show empty state
            console.log('No units found, showing empty state');
            const emptyMessage = document.createElement('div');
            emptyMessage.className = 'placeholder-content';
            emptyMessage.innerHTML = 'No units in this squad.';
            unitsList.appendChild(emptyMessage);
        } else {
            // Create unit display boxes
            console.log(`Creating display for ${units.length} units`);
            units.forEach((unit, index) => {
                console.log(`Unit ${index}:`, unit);
                const unitBox = document.createElement('div');
                unitBox.className = 'unit-display-box';
                
                unitBox.innerHTML = `
                    <div class="unit-name">${unit.name || 'Unnamed Unit'}</div>
                    <div class="unit-details">
                        <div class="unit-detail"><strong>Race:</strong> ${unit.race || 'None'}</div>
                        <div class="unit-detail"><strong>Class:</strong> ${unit.class || 'Basic'}</div>
                        <div class="unit-detail"><strong>Level:</strong> ${unit.level || 1}</div>
                        <div class="unit-detail"><strong>Armor:</strong> ${unit.armor || 'None'}</div>
                        <div class="unit-detail"><strong>Weapon:</strong> ${unit.weapon || 'None'}</div>
                        <div class="unit-detail"><strong>HP:</strong> ${unit.hp || 'N/A'}</div>
                    </div>
                `;
                
                unitsList.appendChild(unitBox);
            });
        }
    }

    // ============================
    // FORM MANAGEMENT
    // ============================

    showCreateForm() {
        /**
         * Show the creation form, hide other content
         */
        document.getElementById('squad-units-container').style.display = 'none';
        document.getElementById('create-form-container').style.display = 'block';
        
        // Clear selection
        document.querySelectorAll('.squad-box').forEach(box => {
            box.classList.remove('selected');
        });
        this.selectedSquad = null;
        
        // Reset unit counter
        this.unitCounter = 0;
        
        // Update the Add Unit button
        this.updateAddUnitButton();
        
        // Focus on the name field
        document.getElementById('squad-name').focus();
        console.log("Showing create form");
    }

    hideCreateForm() {
        /**
         * Hide the creation form, show appropriate content
         */
        document.getElementById('create-form-container').style.display = 'none';
        
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
        // Check if we already have 4 units (limit)
        const existingUnits = document.querySelectorAll('.unit-form');
        if (existingUnits.length >= 4) {
            alert('Maximum of 4 units per squad allowed!');
            return;
        }
        
        this.unitCounter++;
        const unitId = `unit-${this.unitCounter}`;
        
        const unitsContainer = document.getElementById('units-container');
        
        const unitForm = document.createElement('div');
        unitForm.className = 'unit-form';
        unitForm.id = unitId;
        
        unitForm.innerHTML = `
            <div class="unit-form-header">
                <input type="text" class="unit-name-input" id="${unitId}-name" placeholder="Enter unit name..." autocomplete="off">
                <button type="button" class="remove-unit-btn" onclick="removeUnitForm('${unitId}')">×</button>
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
        
        // Add event listeners for the name input
        const nameInput = document.getElementById(`${unitId}-name`);
        nameInput.addEventListener('blur', () => this.handleNameBlur(unitId));
        nameInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                nameInput.blur(); // Trigger the blur event
            }
        });
        
        // Focus on the name input
        nameInput.focus();
        
        // Update the Add Unit button
        this.updateAddUnitButton();
        
        console.log(`Added unit form ${this.unitCounter}`);
    }
    
    updateAddUnitButton() {
        /**
         * Update the Add Unit button to show current count and disable if at limit
         */
        const existingUnits = document.querySelectorAll('.unit-form');
        const addUnitBtn = document.querySelector('.btn-add-unit');
        
        if (addUnitBtn) {
            const count = existingUnits.length;
            if (count >= 4) {
                addUnitBtn.textContent = `+ Add Unit (${count}/4) - MAX REACHED`;
                addUnitBtn.disabled = true;
                addUnitBtn.style.opacity = '0.5';
            } else {
                addUnitBtn.textContent = `+ Add Unit (${count}/4)`;
                addUnitBtn.disabled = false;
                addUnitBtn.style.opacity = '1';
            }
        }
    }

    generateOptions(items) {
        /**
         * Generate HTML option elements for dropdowns
         */
        return items.map(item => 
            `<option value="${item.name}">${item.name}</option>`
        ).join('');
    }

    handleNameBlur(unitId) {
        /**
         * Handle when user clicks out of or presses Enter in the name input
         */
        const nameInput = document.getElementById(`${unitId}-name`);
        const unitName = nameInput.value.trim();
        
        if (unitName) {
            // Convert input to header
            const header = nameInput.parentElement;
            nameInput.style.display = 'none';
            
            // Create or update the name header
            let nameHeader = header.querySelector('.unit-name-header');
            if (!nameHeader) {
                nameHeader = document.createElement('span');
                nameHeader.className = 'unit-name-header';
                nameHeader.addEventListener('click', () => this.editUnitName(unitId));
                header.insertBefore(nameHeader, nameInput);
            }
            nameHeader.textContent = unitName;
            nameHeader.style.display = 'inline';
        }
    }

    editUnitName(unitId) {
        /**
         * Allow user to edit unit name by clicking on the header
         */
        const header = document.querySelector(`#${unitId} .unit-form-header`);
        const nameInput = document.getElementById(`${unitId}-name`);
        const nameHeader = header.querySelector('.unit-name-header');
        
        // Hide header and show input
        nameHeader.style.display = 'none';
        nameInput.style.display = 'inline';
        nameInput.focus();
        nameInput.select(); // Select all text for easy editing
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
        
        // Validate unit count
        if (units.length > 4) {
            alert('Maximum of 4 units per squad allowed!');
            return;
        }

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
        
        // Update the Add Unit button
        app.updateAddUnitButton();
    }
}

// ============================
// ABOUT POPUP FUNCTIONS
// ============================

function showAboutPopup() {
    document.getElementById('about-popup').style.display = 'flex';
    console.log("Showing about popup");
}

function hideAboutPopup() {
    document.getElementById('about-popup').style.display = 'none';
    console.log("Hiding about popup");
}

// ============================
// BATTLE REPORT POPUP FUNCTIONS
// ============================

async function showBattleReportPopup() {
    console.log("Showing battle report popup");
    
    // Show the popup first
    document.getElementById('battle-report-popup').style.display = 'flex';
    
    // Show loading state
    const popupBody = document.querySelector('#battle-report-popup .popup-body');
    popupBody.innerHTML = '<p>Loading battle report...</p>';
    
    try {
        // Fetch the latest battle report
        const response = await fetch(`${app.apiUrl}/battle-report`);
        const data = await response.json();
        
        if (response.ok) {
            // Display the battle report content
            displayBattleReport(data);
        } else {
            // Show error message
            popupBody.innerHTML = `
                <p><strong>Error loading battle report:</strong></p>
                <p>${data.error || 'Unknown error occurred'}</p>
            `;
        }
    } catch (error) {
        console.error('Error fetching battle report:', error);
        popupBody.innerHTML = `
            <p><strong>Error loading battle report:</strong></p>
            <p>Failed to connect to server. Please try again later.</p>
        `;
    }
}

function displayBattleReport(data) {
    const popupBody = document.querySelector('#battle-report-popup .popup-body');
    
    if (!data.content || data.content === "No battle reports found.") {
        popupBody.innerHTML = `
            <p><strong>No Battle Reports Available</strong></p>
            <p>No recent battles have been recorded. Battles occur automatically every 2 hours when there are enough squads in the system.</p>
            
            <h4>Battle System:</h4>
            <ul>
                <li>Battles are automatically scheduled every 2 hours</li>
                <li>Requires a minimum number of squads to trigger</li>
                <li>Squads compete based on their unit composition and stats</li>
                <li>Winners gain experience and ranking</li>
            </ul>
            
            <h4>Next Battle:</h4>
            <p><em>Waiting for sufficient squads to be created...</em></p>
            
            <p><strong>Current Status:</strong> Battle system is active and monitoring for new squads.</p>
        `;
        return;
    }
    
    // Format the battle report content
    const lines = data.content.split('\n');
    let formattedContent = '';
    
    // Add header with timestamp if available
    if (data.timestamp) {
        const dateStr = data.timestamp.substring(0, 8); // YYYYMMDD
        const timeStr = data.timestamp.substring(9, 15); // HHMMSS
        const formattedDate = `${dateStr.substring(0,4)}-${dateStr.substring(4,6)}-${dateStr.substring(6,8)}`;
        const formattedTime = `${timeStr.substring(0,2)}:${timeStr.substring(2,4)}:${timeStr.substring(4,6)}`;
        
        formattedContent += `<p><strong>Battle Report - ${formattedDate} at ${formattedTime}</strong></p>`;
    }
    
    // Process each line of the battle report
    lines.forEach(line => {
        line = line.trim();
        if (!line) return;
        
        // Format different types of lines
        if (line.includes('begin to fight!')) {
            formattedContent += `<h4 style="color: #d4af37; margin: 15px 0 10px 0;">${line}</h4>`;
        } else if (line.includes('has been defeated!')) {
            formattedContent += `<p style="color: #dc3545; font-weight: bold;">${line}</p>`;
        } else if (line.includes('The battle is over!')) {
            formattedContent += `<h4 style="color: #28a745; margin: 15px 0 10px 0;">${line}</h4>`;
        } else if (line.includes('now has') && line.includes('health remaining')) {
            formattedContent += `<p style="color: #6c757d; margin-left: 20px;">${line}</p>`;
        } else if (line.includes('now attacks')) {
            formattedContent += `<p style="color: #007bff; font-weight: bold; margin: 10px 0 5px 0;">${line}</p>`;
        } else if (line.includes('rolls a') && (line.includes('to attack') || line.includes('to defend'))) {
            formattedContent += `<p style="color: #6c757d; margin-left: 20px; font-style: italic;">${line}</p>`;
        } else {
            formattedContent += `<p>${line}</p>`;
        }
    });
    
    popupBody.innerHTML = formattedContent;
}

function hideBattleReportPopup() {
    document.getElementById('battle-report-popup').style.display = 'none';
    console.log("Hiding battle report popup");
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
    
    // Add Escape key support for popup closing
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            if (document.getElementById('about-popup').style.display !== 'none') {
                hideAboutPopup();
            }
            if (document.getElementById('battle-report-popup').style.display !== 'none') {
                hideBattleReportPopup();
            }
        }
    });
    
    // Close popup when clicking outside of it
    document.addEventListener('click', function(e) {
        const aboutPopup = document.getElementById('about-popup');
        const battleReportPopup = document.getElementById('battle-report-popup');
        
        if (e.target === aboutPopup) {
            hideAboutPopup();
        }
        if (e.target === battleReportPopup) {
            hideBattleReportPopup();
        }
    });
}); 