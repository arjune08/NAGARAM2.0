/*
 * NAGARAM — Main Client-Side JavaScript & i18n Engine
 */

// ─── Multilingual Dictionary (English, Tamil, Hindi) ──────────────────
const translations = {
    en: {
        how_it_works: "How It Works",
        capabilities: "Capabilities",
        portals: "Portals",
        faq: "FAQ",
        sign_in: "Sign In",
        get_started: "Get Started",
        my_dashboard: "My Dashboard →",
        tagline: "Flagship Intelligent Platform for Civic & Agricultural Action",
        description: "Connecting Citizens, Farmers, Experts, NGOs, Volunteers, and Authorities through real-time AI disease diagnostics, GIS issue triage, live market intelligence, and coordinated field action.",
        citizen_portal: "Citizen Portal",
        farmer_portal: "Farmer Portal",
        expert_network: "Expert Network",
        ngo_coordination: "NGO Coordination",
        volunteer_hub: "Volunteer Hub",
        admin_portal: "Administration"
    },
    ta: {
        how_it_works: "செயல்படும் முறை",
        capabilities: "சேவைகள்",
        portals: "தளங்கள்",
        faq: "கேள்விகள்",
        sign_in: "உள்நுழைவு",
        get_started: "தொடங்குங்கள்",
        my_dashboard: "எனது முகப்பு →",
        tagline: "குடிமக்கள் மற்றும் விவசாயிகளுக்கான ஒருங்கிணைந்த புத்திசாலித்தனமான தளம்",
        description: "குடிமக்கள், விவசாயிகள், வல்லுநர்கள், தொண்டு நிறுவனங்கள் மற்றும் அரசு அதிகாரிகளை இணைக்கும் தமிழ்நாட்டின் முன்னணி தளம்.",
        citizen_portal: "குடிமக்கள் தளம்",
        farmer_portal: "விவசாயிகள் தளம்",
        expert_network: "வல்லுநர் நெட்வொர்க்",
        ngo_coordination: "தொண்டு நிறுவன தளம்",
        volunteer_hub: "தன்னார்வலர் மையம்",
        admin_portal: "நிர்வாக தளம்"
    },
    hi: {
        how_it_works: "यह कैसे काम करता है",
        capabilities: "सुविधाएं",
        portals: "पोर्टल",
        faq: "सामान्य प्रश्न",
        sign_in: "साइन इन करें",
        get_started: "शुरू करें",
        my_dashboard: "मेरा डैशबोर्ड →",
        tagline: "नागरिक और कृषि सुधार के लिए एकीकृत बुद्धिमान मंच",
        description: "नागरिकों, किसानों, विशेषज्ञों, गैर सरकारी संगठनों, स्वयंसेवकों और अधिकारियों को जोड़ने वाला एकीकृत मंच।",
        citizen_portal: "नागरिक पोर्टल",
        farmer_portal: "किसान पोर्टल",
        expert_network: "विशेषज्ञ नेटवर्क",
        ngo_coordination: "एनजीओ पोर्टल",
        volunteer_hub: "स्वयंसेवक हब",
        admin_portal: "प्रशासन पोर्टल"
    }
};

function changeLanguage(lang) {
    localStorage.setItem('nagaram_lang', lang);
    
    // Update selectors
    document.querySelectorAll('.lang-selector').forEach(sel => {
        sel.value = lang;
    });

    const dict = translations[lang] || translations.en;

    // Translate elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(elem => {
        const key = elem.getAttribute('data-i18n');
        if (dict[key]) {
            elem.innerText = dict[key];
        }
    });

    // Dynamic headline update if present
    const taglineElem = document.querySelector('.hero .tagline');
    if (taglineElem && dict.tagline) {
        taglineElem.innerText = dict.tagline;
    }
}

document.addEventListener('DOMContentLoaded', function () {
    // ─── Initialize Saved Language ───────────────────────────
    const savedLang = localStorage.getItem('nagaram_lang') || 'en';
    changeLanguage(savedLang);

    // ─── Mobile Sidebar Toggle ──────────────────────────────
    const toggleBtn = document.getElementById('mobile-menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function () {
            sidebar.classList.toggle('open');
            if (overlay) overlay.classList.toggle('active');
        });
    }

    if (overlay) {
        overlay.addEventListener('click', function () {
            if (sidebar) sidebar.classList.remove('open');
            overlay.classList.remove('active');
        });
    }

    // ─── Auto-dismiss Flash Messages ───────────────────────
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s';
            setTimeout(function () { alert.remove(); }, 500);
        }, 5000);
    });

    // ─── Offline Indicator ─────────────────────────────────
    const offlineBar = document.getElementById('offline-bar');
    function updateOnlineStatus() {
        if (offlineBar) {
            if (navigator.onLine) {
                offlineBar.classList.remove('visible');
            } else {
                offlineBar.classList.add('visible');
            }
        }
    }
    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);
    updateOnlineStatus();

    // ─── Tabs Handler ──────────────────────────────────────
    const tabButtons = document.querySelectorAll('.tab');
    tabButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const targetId = btn.getAttribute('data-tab');
            const parent = btn.closest('.tabs-container') || document;

            parent.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            parent.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const targetPanel = parent.querySelector('#' + targetId);
            if (targetPanel) targetPanel.classList.add('active');
        });
    });
});
