/* ==========================================================================
   AI Multi-Agent E-Commerce Studio - Client Side JS Engine
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function () {
    initComparisonTray();
});

/* --- Password Toggle --- */
function togglePasswordVisibility(fieldId, btnElement) {
    const field = document.getElementById(fieldId);
    const icon = btnElement.querySelector("i");

    if (field.type === "password") {
        field.type = "text";
        icon.className = "fa-solid fa-eye-slash";
    } else {
        field.type = "password";
        icon.className = "fa-solid fa-eye";
    }
}

/* --- Password Strength Meter --- */
function checkPasswordStrength(password) {
    const bar = document.getElementById("strengthBar");
    const text = document.getElementById("strengthText");
    if (!bar || !text) return;

    let score = 0;
    if (password.length >= 6) score += 25;
    if (password.length >= 10) score += 25;
    if (/[A-Z]/.test(password)) score += 15;
    if (/[0-9]/.test(password)) score += 15;
    if (/[^A-Za-z0-9]/.test(password)) score += 20;

    bar.style.width = score + "%";

    if (score < 40) {
        bar.style.backgroundColor = "#f43f5e";
        text.innerText = "Password Strength: Weak (min 6 characters)";
        text.style.color = "#f43f5e";
    } else if (score < 75) {
        bar.style.backgroundColor = "#fbbf24";
        text.innerText = "Password Strength: Medium";
        text.style.color = "#fbbf24";
    } else {
        bar.style.backgroundColor = "#10b981";
        text.innerText = "Password Strength: Strong";
        text.style.color = "#10b981";
    }
}

function validatePasswordMatch() {
    const p1 = document.getElementById("password") ? document.getElementById("password").value : "";
    const p2 = document.getElementById("confirm_password") ? document.getElementById("confirm_password").value : "";
    const msg = document.getElementById("matchMsg");
    if (!msg) return true;

    if (p2 && p1 !== p2) {
        msg.innerText = "Passwords do not match.";
        msg.style.color = "#f43f5e";
        return false;
    } else if (p2 && p1 === p2) {
        msg.innerText = "Passwords match.";
        msg.style.color = "#10b981";
        return true;
    }
    return true;
}

function validateRegistrationForm() {
    const p1 = document.getElementById("password") ? document.getElementById("password").value : "";
    const p2 = document.getElementById("confirm_password") ? document.getElementById("confirm_password").value : "";
    
    if (p1.length < 6) {
        alert("Password must be at least 6 characters long.");
        return false;
    }
    if (p1 !== p2) {
        alert("Passwords do not match.");
        return false;
    }
    return true;
}

/* --- Live vs Demo Mode Toggle --- */
function toggleLiveMode(isLive) {
    fetch('/api/toggle-live-mode', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_live: isLive })
    })
    .then(res => res.json())
    .then(data => {
        const textEl = document.getElementById("modeStatusText");
        if (textEl) {
            textEl.innerHTML = data.is_live ? "⚡ Live Market Feed" : "📦 Demo Catalog (50+ items)";
        }
        window.location.reload();
    })
    .catch(err => console.error("Mode toggle failed:", err));
}

/* --- Prompt Chips Helper --- */
function setSearchPrompt(promptText) {
    const input = document.getElementById("nlQueryInput");
    if (input) {
        input.value = promptText;
        input.focus();
    }
}

/* --- Comparison Tray Management --- */
function getComparisonTray() {
    try {
        return JSON.parse(localStorage.getItem("shopagent_compare_tray")) || [];
    } catch (e) {
        return [];
    }
}

function saveComparisonTray(tray) {
    localStorage.setItem("shopagent_compare_tray", JSON.stringify(tray));
    updateComparisonTrayUI();
}

function addToComparison(product) {
    let tray = getComparisonTray();
    if (tray.some(p => p.id === product.id)) {
        alert(`${product.name} is already in your comparison list.`);
        return;
    }

    if (tray.length >= 4) {
        alert("You can compare up to 4 products at a time. Remove one to add another.");
        return;
    }

    tray.push(product);
    saveComparisonTray(tray);
    
    // Sync with backend session
    syncTrayWithBackend(tray);
}

function removeFromComparisonTray(productId) {
    let tray = getComparisonTray();
    tray = tray.filter(p => p.id !== productId);
    saveComparisonTray(tray);
    syncTrayWithBackend(tray);
}

function clearComparisonTray() {
    saveComparisonTray([]);
    syncTrayWithBackend([]);
}

function syncTrayWithBackend(tray) {
    const ids = tray.map(p => p.id);
    fetch('/api/update-compare-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_ids: ids })
    })
    .catch(err => console.error("Tray sync error:", err));
}

function updateComparisonTrayUI() {
    const tray = getComparisonTray();
    const trayElement = document.getElementById("comparisonTray");
    const countBadge = document.getElementById("compareCountBadge");
    const trayCount = document.getElementById("trayCount");
    const container = document.getElementById("trayItemsContainer");

    if (countBadge) countBadge.innerText = tray.length;
    if (trayCount) trayCount.innerText = tray.length;

    if (!trayElement) return;

    if (tray.length > 0) {
        trayElement.style.display = "block";
        if (container) {
            container.innerHTML = tray.map(p => `
                <div class="tray-item-chip">
                    <span>${p.name.substring(0, 18)}...</span>
                    <button type="button" onclick="removeFromComparisonTray('${p.id}')" style="background:none; border:none; color:#f43f5e; cursor:pointer;">&times;</button>
                </div>
            `).join('');
        }
    } else {
        trayElement.style.display = "none";
    }
}

function initComparisonTray() {
    updateComparisonTrayUI();
}
