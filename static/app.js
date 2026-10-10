document.addEventListener('DOMContentLoaded', () => {
    // Initial Auth Check
    checkAuthState();

    loadCategories();
    fetchCatalog();

    const reqForm = document.getElementById('requirement-form');
    if (reqForm) {
        reqForm.addEventListener('submit', handlePipelineSubmit);
    }

    const filterBtn = document.getElementById('catalog-filter-btn');
    if (filterBtn) {
        filterBtn.addEventListener('click', fetchCatalog);
    }

    const compareBtn = document.getElementById('compare-selected-btn');
    if (compareBtn) {
        compareBtn.addEventListener('click', handleManualCompare);
    }

    document.querySelectorAll('.sample-prompt-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const cleanText = btn.innerText.replace(/^[\u2600-\u27BF\uE000-\uF8FF\uD83C-\uDBFF\uDC00-\uDFFF]\s*/, '').trim();
            const input = document.getElementById('requirement-input');
            if (input) input.value = cleanText;
        });
    });
});

let selectedProductIds = new Set();
let currentPipelineData = null;
let currentUser = null;

function getCategoryFallbackImage(category) {
    const cat = (category || '').toLowerCase();
    if (cat.includes('laptop')) return '/static/images/laptop.svg';
    if (cat.includes('phone') || cat.includes('mobile')) return '/static/images/smartphone.svg';
    if (cat.includes('headphone') || cat.includes('audio')) return '/static/images/headphones.svg';
    if (cat.includes('monitor') || cat.includes('display')) return '/static/images/monitor.svg';
    if (cat.includes('furniture') || cat.includes('chair')) return '/static/images/furniture.svg';
    return '/static/images/laptop.svg';
}

function formatRupees(amount) {
    if (amount === undefined || amount === null) return 'N/A';
    return '₹' + Number(amount).toLocaleString('en-IN');
}

function switchAuthPageTab(tab) {
    const signinForm = document.getElementById('auth-page-signin-form');
    const signupForm = document.getElementById('auth-page-signup-form');
    const tabSignin = document.getElementById('auth-tab-signin');
    const tabSignup = document.getElementById('auth-tab-signup');

    if (tab === 'signin') {
        if (signinForm) signinForm.classList.remove('hidden');
        if (signupForm) signupForm.classList.add('hidden');
        if (tabSignin) tabSignin.className = "w-1/2 py-3 font-black text-base text-purple-700 border-b-2 border-purple-600 transition";
        if (tabSignup) tabSignup.className = "w-1/2 py-3 font-semibold text-base text-slate-500 border-b-2 border-transparent hover:text-slate-800 transition";
    } else {
        if (signupForm) signupForm.classList.remove('hidden');
        if (signinForm) signinForm.classList.add('hidden');
        if (tabSignup) tabSignup.className = "w-1/2 py-3 font-black text-base text-purple-700 border-b-2 border-purple-600 transition";
        if (tabSignin) tabSignin.className = "w-1/2 py-3 font-semibold text-base text-slate-500 border-b-2 border-transparent hover:text-slate-800 transition";
    }
}

function handleAuthPageSubmit(e, type) {
    if (e && e.preventDefault) e.preventDefault();
    demoQuickLogin();
    return false;
}

function demoQuickLogin() {
    currentUser = { name: 'Alex Johnson', email: 'alex@example.com' };
    localStorage.setItem('user_auth', JSON.stringify(currentUser));
    forceOpenDashboard();
}

function forceOpenDashboard() {
    const authPage = document.getElementById('auth-page');
    const mainContent = document.getElementById('app-main-content');
    const container = document.getElementById('auth-nav-container');
    const welcomeBadge = document.getElementById('user-welcome-badge');

    if (authPage) {
        authPage.classList.add('hidden');
        authPage.style.setProperty('display', 'none', 'important');
    }
    if (mainContent) {
        mainContent.classList.remove('hidden');
        mainContent.style.setProperty('display', 'block', 'important');
    }

    if (container) {
        const name = currentUser ? currentUser.name : 'Alex Johnson';
        container.innerHTML = `
            <div class="flex items-center space-x-2 bg-purple-50 px-3.5 py-1.5 rounded-xl border border-purple-200">
                <div class="w-7 h-7 rounded-full bg-purple-600 text-white flex items-center justify-center font-bold text-xs shadow-sm">
                    ${name.charAt(0).toUpperCase()}
                </div>
                <span class="text-xs font-bold text-slate-800">${name}</span>
                <button onclick="handleLogout()" class="text-slate-400 hover:text-rose-600 text-xs ml-1 font-semibold" title="Sign Out">
                    <i class="fa-solid fa-right-from-bracket mr-1"></i> Sign Out
                </button>
            </div>
        `;
    }

    if (welcomeBadge) {
        welcomeBadge.textContent = `Welcome back, ${currentUser ? currentUser.name : 'Alex'}!`;
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function capitalize(str) {
    if (!str) return 'User';
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function checkAuthState() {
    const saved = localStorage.getItem('user_auth');
    if (saved) {
        try {
            currentUser = JSON.parse(saved);
        } catch(e) {
            currentUser = null;
        }
    }
    updateAuthUI();
}

function updateAuthUI() {
    if (currentUser) {
        forceOpenDashboard();
    } else {
        const authPage = document.getElementById('auth-page');
        const mainContent = document.getElementById('app-main-content');
        const container = document.getElementById('auth-nav-container');

        if (authPage) {
            authPage.classList.remove('hidden');
            authPage.style.setProperty('display', 'flex', 'important');
        }
        if (mainContent) {
            mainContent.classList.add('hidden');
            mainContent.style.setProperty('display', 'none', 'important');
        }

        if (container) {
            container.innerHTML = `
                <button onclick="demoQuickLogin()" class="px-4 py-2 bg-purple-600 text-white text-xs font-bold rounded-lg shadow hover:bg-purple-700 transition">
                    Open Dashboard <i class="fa-solid fa-arrow-right ml-1"></i>
                </button>
            `;
        }
    }
}

function handleLogout() {
    currentUser = null;
    localStorage.removeItem('user_auth');
    updateAuthUI();
}

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Load Categories
async function loadCategories() {
    try {
        const resp = await fetch('/api/categories');
        const data = await resp.json();
        const select = document.getElementById('catalog-category-filter');
        if (select) {
            select.innerHTML = '<option value="All">All Categories</option>';
            data.categories.forEach(cat => {
                const opt = document.createElement('option');
                opt.value = cat;
                opt.textContent = cat;
                select.appendChild(opt);
            });
        }
    } catch (err) {
        console.error("Failed to load categories:", err);
    }
}

// Fetch Catalog Products
async function fetchCatalog() {
    const catElem = document.getElementById('catalog-category-filter');
    const priceElem = document.getElementById('catalog-max-price');
    const searchElem = document.getElementById('catalog-search-input');

    const category = catElem ? catElem.value : 'All';
    const maxPrice = priceElem ? priceElem.value : '';
    const search = searchElem ? searchElem.value : '';

    let url = `/api/products?1=1`;
    if (category && category !== 'All') url += `&category=${encodeURIComponent(category)}`;
    if (maxPrice) url += `&max_price=${maxPrice}`;
    if (search) url += `&search=${encodeURIComponent(search)}`;

    try {
        const resp = await fetch(url);
        const data = await resp.json();
        renderCatalogGrid(data.products);
    } catch (err) {
        console.error("Error fetching catalog:", err);
    }
}

function renderCatalogGrid(products) {
    const grid = document.getElementById('catalog-grid');
    if (!grid) return;

    grid.innerHTML = '';

    if (!products || products.length === 0) {
        grid.innerHTML = `<div class="col-span-full py-8 text-center text-slate-500">No products match the selected criteria.</div>`;
        return;
    }

    products.forEach(p => {
        const isChecked = selectedProductIds.has(p.id);
        const card = document.createElement('div');
        card.className = "bg-white border border-slate-200 rounded-xl p-4 shadow-sm hover:shadow-md transition flex flex-col justify-between group";
        
        const tagsHtml = (p.tags || []).slice(0, 3).map(t => 
            `<span class="px-2 py-0.5 bg-slate-100 text-slate-700 text-[10px] font-semibold rounded border border-slate-200">${t}</span>`
        ).join(' ');

        const fallbackImg = getCategoryFallbackImage(p.category);
        const imgUrl = p.image_url || fallbackImg;

        card.innerHTML = `
            <div>
                <div class="relative mb-3 overflow-hidden rounded-lg bg-slate-100 h-44 border border-slate-200">
                    <img src="${imgUrl}" alt="${p.name}" 
                         onerror="this.onerror=null; this.src='${fallbackImg}';"
                         class="w-full h-full object-cover group-hover:scale-105 transition duration-300">
                    <span class="absolute top-2 left-2 text-[10px] font-bold px-2 py-0.5 rounded bg-white/90 text-purple-800 shadow-sm border border-purple-200">${p.category}</span>
                    <label class="absolute top-2 right-2 inline-flex items-center space-x-1 cursor-pointer bg-white/90 px-2 py-0.5 rounded shadow-sm border border-slate-200">
                        <input type="checkbox" value="${p.id}" ${isChecked ? 'checked' : ''} onchange="toggleSelectProduct('${p.id}')"
                            class="w-3.5 h-3.5 rounded border-slate-300 text-purple-600 focus:ring-purple-500">
                        <span class="text-[10px] font-bold text-slate-700">Compare</span>
                    </label>
                </div>
                <h4 class="font-bold text-slate-900 text-base mb-0.5 line-clamp-1">${p.name}</h4>
                <div class="text-xs text-slate-500 font-medium mb-2">${p.brand} • ★ ${p.rating} (${p.review_count})</div>
                <p class="text-xs text-slate-600 line-clamp-2 mb-3">${p.description || ''}</p>
                <div class="flex flex-wrap gap-1 mb-3">${tagsHtml}</div>
            </div>
            <div class="pt-3 border-t border-slate-100 flex items-center justify-between">
                <span class="text-base font-black text-slate-900">${formatRupees(p.price)}</span>
                <button onclick="quickAnalyzeSingle('${p.name}')" class="text-xs text-purple-700 hover:text-purple-900 font-bold">
                    Analyze <i class="fa-solid fa-arrow-right ml-1"></i>
                </button>
            </div>
        `;
        grid.appendChild(card);
    });
}

function toggleSelectProduct(pid) {
    if (selectedProductIds.has(pid)) {
        selectedProductIds.delete(pid);
    } else {
        selectedProductIds.add(pid);
    }
    const countSpan = document.getElementById('selected-count');
    const compareBtn = document.getElementById('compare-selected-btn');
    if (countSpan) countSpan.textContent = selectedProductIds.size;
    if (compareBtn) {
        if (selectedProductIds.size > 1) {
            compareBtn.classList.remove('hidden');
        } else {
            compareBtn.classList.add('hidden');
        }
    }
}

async function quickAnalyzeSingle(productName) {
    const input = document.getElementById('requirement-input');
    if (input) input.value = `Compare ${productName} against similar alternatives and recommend the best option.`;
    const form = document.getElementById('requirement-form');
    if (form) form.dispatchEvent(new Event('submit'));
}

async function handleManualCompare() {
    if (selectedProductIds.size < 2) return;
    const pids = Array.from(selectedProductIds);

    showPipelineUI();
    updateStepStatus(1, 'active', 'Analyzing manual product selections...');
    
    try {
        const resp = await fetch('/api/compare', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ product_ids: pids })
        });
        const data = await resp.json();
        
        updateStepStatus(1, 'done', 'Products loaded');
        updateStepStatus(2, 'done', `Filtered ${data.candidates.length} items`);
        updateStepStatus(3, 'done', 'Matrix generated');

        renderResults(data.candidates, data.comparison);
    } catch (err) {
        console.error("Compare error:", err);
    }
}

// Pipeline Submission
async function handlePipelineSubmit(e) {
    e.preventDefault();
    const input = document.getElementById('requirement-input');
    const reqText = input ? input.value.trim() : '';
    if (!reqText) return;

    showPipelineUI();

    resetStepUI(1, 'Agent 1: Requirements Analyst', 'Extracting constraints & budget limits in Rupees (₹)...');
    resetStepUI(2, 'Agent 2: Catalog Filter', 'Searching SQLite database...');
    resetStepUI(3, 'Agent 3: Comparison Synthesizer', 'Building spec matrix & recommendations...');

    updateStepStatus(1, 'active', 'Running NLP Extraction...');

    try {
        const resp = await fetch('/api/pipeline/run', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ requirement_text: reqText })
        });

        const data = await resp.json();
        currentPipelineData = data;

        const trace1 = data.pipeline_traces.find(t => t.step === 1);
        updateStepStatus(1, 'done', trace1 ? trace1.output_summary : 'Extraction Complete');
        const trace1Elem = document.getElementById('step-1-trace');
        if (trace1Elem) trace1Elem.textContent = trace1 ? trace1.thought_trace : '';

        const trace2 = data.pipeline_traces.find(t => t.step === 2);
        updateStepStatus(2, 'done', trace2 ? trace2.output_summary : 'Search Complete');
        const trace2Elem = document.getElementById('step-2-trace');
        if (trace2Elem) trace2Elem.textContent = trace2 ? trace2.thought_trace : '';

        const trace3 = data.pipeline_traces.find(t => t.step === 3);
        updateStepStatus(3, 'done', trace3 ? trace3.output_summary : 'Synthesis Complete');
        const trace3Elem = document.getElementById('step-3-trace');
        if (trace3Elem) trace3Elem.textContent = trace3 ? trace3.thought_trace : '';

        renderResults(data.candidates, data.comparison);

    } catch (err) {
        console.error("Pipeline error:", err);
        updateStepStatus(1, 'error', 'Pipeline execution failed.');
    }
}

function showPipelineUI() {
    const traces = document.getElementById('pipeline-traces-container');
    const results = document.getElementById('results-container');
    if (traces) traces.classList.remove('hidden');
    if (results) {
        results.classList.remove('hidden');
        results.scrollIntoView({ behavior: 'smooth' });
    }
}

function resetStepUI(stepNum, title, summary) {
    const card = document.getElementById(`step-${stepNum}-card`);
    if (card) card.className = "bg-white border border-slate-200 rounded-xl p-4 shadow-sm transition opacity-60";
    const status = document.getElementById(`step-${stepNum}-status`);
    if (status) status.innerHTML = 'Queued';
    const sumElem = document.getElementById(`step-${stepNum}-summary`);
    if (sumElem) sumElem.textContent = summary;
    const traceElem = document.getElementById(`step-${stepNum}-trace`);
    if (traceElem) traceElem.textContent = 'Waiting...';
}

function updateStepStatus(stepNum, state, summaryText) {
    const card = document.getElementById(`step-${stepNum}-card`);
    const statusSpan = document.getElementById(`step-${stepNum}-status`);
    const summaryP = document.getElementById(`step-${stepNum}-summary`);

    if (summaryP && summaryText) summaryP.textContent = summaryText;

    if (card && statusSpan) {
        if (state === 'active') {
            card.className = "bg-white border-2 border-purple-600 rounded-xl p-4 shadow-md transition agent-step-active";
            statusSpan.innerHTML = `<i class="fa-solid fa-spinner fa-spin text-purple-600 mr-1"></i> Running...`;
        } else if (state === 'done') {
            card.className = "bg-white border-2 border-emerald-500 rounded-xl p-4 shadow-md transition agent-step-done";
            statusSpan.innerHTML = `<i class="fa-solid fa-check text-emerald-600 mr-1"></i> Complete`;
        } else if (state === 'error') {
            card.className = "bg-white border-2 border-rose-500 rounded-xl p-4 shadow-md transition";
            statusSpan.innerHTML = `<i class="fa-solid fa-circle-exclamation text-rose-600 mr-1"></i> Error`;
        }
    }
}

function renderResults(candidates, comparison) {
    const winner = comparison.winner_overall;
    if (winner) {
        const winnerFallback = getCategoryFallbackImage(winner.category);
        const nameElem = document.getElementById('winner-name');
        const scoreElem = document.getElementById('winner-score');
        const priceElem = document.getElementById('winner-price');
        const sumElem = document.getElementById('winner-summary');
        
        if (nameElem) nameElem.textContent = winner.name;
        if (scoreElem) scoreElem.textContent = `${winner.match_score}%`;
        if (priceElem) priceElem.textContent = formatRupees(winner.price);
        if (sumElem) sumElem.textContent = comparison.summary_narrative || '';
        
        const winnerImg = document.getElementById('winner-img');
        if (winnerImg) {
            winnerImg.onerror = function() { this.onerror=null; this.src = winnerFallback; };
            winnerImg.src = winner.image_url || winnerFallback;
        }
    }

    renderSpecMatrix(candidates, comparison.comparison_matrix, winner ? winner.id : null);
    renderProsCons(candidates, comparison.pros_cons || {});
    renderCandidateCards(candidates, winner ? winner.id : null);
}

function renderSpecMatrix(candidates, matrix, winnerId) {
    const headerRow = document.getElementById('matrix-header-row');
    const tbody = document.getElementById('matrix-body');
    if (!headerRow || !tbody) return;

    headerRow.innerHTML = `<th class="p-4 w-48 font-bold bg-slate-100 border-r border-slate-300">Feature / Spec</th>`;

    candidates.forEach(c => {
        const isWinner = c.id === winnerId;
        const fallbackImg = getCategoryFallbackImage(c.category);
        const th = document.createElement('th');
        th.className = `p-4 font-bold border-r border-slate-300 min-w-[200px] ${isWinner ? 'table-winner-col' : ''}`;
        th.innerHTML = `
            <div class="flex items-center space-x-3 mb-2">
                <img src="${c.image_url || fallbackImg}" 
                     onerror="this.onerror=null; this.src='${fallbackImg}';"
                     alt="${c.name}" class="w-10 h-10 object-cover rounded-lg border border-slate-300 shadow-sm shrink-0">
                <div>
                    <div class="flex items-center space-x-1">
                        <span class="text-slate-900 font-bold">${c.name}</span>
                        ${isWinner ? '<span class="text-[9px] px-1.5 py-0.5 rounded bg-purple-600 text-white font-bold">WINNER</span>' : ''}
                    </div>
                    <div class="text-xs text-slate-600 font-medium">${c.brand} • ${formatRupees(c.price)}</div>
                </div>
            </div>
        `;
        headerRow.appendChild(th);
    });

    tbody.innerHTML = '';
    matrix.forEach(row => {
        const tr = document.createElement('tr');
        tr.className = "hover:bg-purple-50/30 transition";
        
        let rowHtml = `<td class="p-4 font-bold text-slate-800 bg-slate-50 border-r border-slate-300">${row.feature}</td>`;
        candidates.forEach(c => {
            const isWinner = c.id === winnerId;
            const val = row.values[c.id] || 'N/A';
            rowHtml += `<td class="p-4 border-r border-slate-200 ${isWinner ? 'table-winner-col font-semibold text-slate-900' : 'text-slate-700'}">${val}</td>`;
        });

        tr.innerHTML = rowHtml;
        tbody.appendChild(tr);
    });
}

function renderProsCons(candidates, prosConsMap) {
    const container = document.getElementById('tab-content-proscons');
    if (!container) return;
    container.innerHTML = '';

    candidates.forEach(c => {
        const pc = prosConsMap[c.id] || { pros: [], cons: [] };
        const fallbackImg = getCategoryFallbackImage(c.category);
        const card = document.createElement('div');
        card.className = "bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4";
        
        const prosList = pc.pros.map(p => `<li class="text-xs text-emerald-800 font-semibold flex items-start"><i class="fa-solid fa-circle-check text-emerald-600 mt-0.5 mr-2"></i> ${p}</li>`).join('');
        const consList = pc.cons.map(cn => `<li class="text-xs text-rose-800 font-semibold flex items-start"><i class="fa-solid fa-circle-xmark text-rose-500 mt-0.5 mr-2"></i> ${cn}</li>`).join('');

        card.innerHTML = `
            <div class="flex items-center space-x-3 border-b border-slate-200 pb-3">
                <img src="${c.image_url || fallbackImg}" 
                     onerror="this.onerror=null; this.src='${fallbackImg}';"
                     alt="${c.name}" class="w-12 h-12 object-cover rounded-lg border border-slate-200 shrink-0">
                <div>
                    <h4 class="font-bold text-slate-900 text-base">${c.name}</h4>
                    <div class="text-xs text-slate-600">${formatRupees(c.price)} • Rating ★ ${c.rating}</div>
                </div>
            </div>
            
            <div class="space-y-2">
                <div class="text-xs font-bold uppercase tracking-wider text-emerald-700">Pros / Key Advantages</div>
                <ul class="space-y-1.5">${prosList || '<li class="text-xs text-slate-500">Standard features</li>'}</ul>
            </div>

            <div class="space-y-2 pt-2 border-t border-slate-100">
                <div class="text-xs font-bold uppercase tracking-wider text-rose-700">Cons / Trade-offs</div>
                <ul class="space-y-1.5">${consList || '<li class="text-xs text-slate-500">No major drawbacks noted</li>'}</ul>
            </div>
        `;
        container.appendChild(card);
    });
}

function renderCandidateCards(candidates, winnerId) {
    const container = document.getElementById('tab-content-candidates');
    if (!container) return;
    container.innerHTML = '';

    candidates.forEach(c => {
        const isWinner = c.id === winnerId;
        const fallbackImg = getCategoryFallbackImage(c.category);
        const card = document.createElement('div');
        card.className = `bg-white border ${isWinner ? 'border-purple-600 ring-2 ring-purple-500/20' : 'border-slate-200'} rounded-2xl p-5 shadow-sm flex flex-col justify-between`;

        const specsBadges = Object.entries(c.specs || {}).map(([k, v]) => 
            `<div class="text-xs bg-slate-50 px-2 py-1 rounded border border-slate-200"><span class="text-slate-500 font-bold uppercase text-[9px]">${k}:</span> <span class="text-slate-900 font-bold">${v}</span></div>`
        ).join('');

        card.innerHTML = `
            <div>
                <div class="relative h-44 overflow-hidden rounded-xl bg-slate-100 mb-3 border border-slate-200">
                    <img src="${c.image_url || fallbackImg}" 
                         onerror="this.onerror=null; this.src='${fallbackImg}';"
                         alt="${c.name}" class="w-full h-full object-cover">
                    <span class="absolute top-2 left-2 text-[10px] font-bold px-2 py-0.5 rounded bg-white/90 text-purple-800 border border-purple-200">${c.category}</span>
                    <span class="absolute top-2 right-2 text-[10px] font-black px-2 py-0.5 rounded bg-emerald-500 text-white shadow-sm">Match: ${c.match_score}%</span>
                </div>
                <h4 class="font-bold text-slate-900 text-lg mb-0.5">${c.name}</h4>
                <div class="text-xs text-slate-600 mb-3">${c.brand} • ★ ${c.rating} (${c.review_count} reviews)</div>
                <p class="text-xs text-slate-600 mb-4 line-clamp-2">${c.description || ''}</p>
                <div class="flex flex-wrap gap-1.5 mb-4">${specsBadges}</div>
            </div>

            <div class="pt-3 border-t border-slate-200 flex items-center justify-between">
                <div class="text-xl font-black text-slate-900">${formatRupees(c.price)}</div>
                ${isWinner ? '<span class="text-xs text-purple-700 font-extrabold"><i class="fa-solid fa-award mr-1"></i> Recommended Winner</span>' : ''}
            </div>
        `;
        container.appendChild(card);
    });
}

function switchTab(tabId) {
    const mat = document.getElementById('tab-content-matrix');
    const pc = document.getElementById('tab-content-proscons');
    const cand = document.getElementById('tab-content-candidates');

    if (mat) mat.classList.add('hidden');
    if (pc) pc.classList.add('hidden');
    if (cand) cand.classList.add('hidden');

    const btnMat = document.getElementById('tab-btn-matrix');
    const btnPc = document.getElementById('tab-btn-proscons');
    const btnCand = document.getElementById('tab-btn-candidates');

    if (btnMat) btnMat.className = "py-3 font-semibold text-sm text-slate-600 border-b-2 border-transparent hover:text-slate-900 transition";
    if (btnPc) btnPc.className = "py-3 font-semibold text-sm text-slate-600 border-b-2 border-transparent hover:text-slate-900 transition";
    if (btnCand) btnCand.className = "py-3 font-semibold text-sm text-slate-600 border-b-2 border-transparent hover:text-slate-900 transition";

    if (tabId === 'matrix-tab') {
        if (mat) mat.classList.remove('hidden');
        if (btnMat) btnMat.className = "py-3 font-bold text-sm text-purple-700 border-b-2 border-purple-600 transition";
    } else if (tabId === 'proscons-tab') {
        if (pc) pc.classList.remove('hidden');
        if (btnPc) btnPc.className = "py-3 font-bold text-sm text-purple-700 border-b-2 border-purple-600 transition";
    } else if (tabId === 'candidates-tab') {
        if (cand) cand.classList.remove('hidden');
        if (btnCand) btnCand.className = "py-3 font-bold text-sm text-purple-700 border-b-2 border-purple-600 transition";
    }
}
