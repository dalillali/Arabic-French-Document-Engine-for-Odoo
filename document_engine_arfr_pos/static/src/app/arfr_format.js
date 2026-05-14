/** @odoo-module **/

const WESTERN_DIGITS = "0123456789";
const ARABIC_INDIC_DIGITS = "٠١٢٣٤٥٦٧٨٩";
const TO_ARABIC_INDIC = Object.fromEntries(
    [...WESTERN_DIGITS].map((digit, index) => [digit, ARABIC_INDIC_DIGITS[index]])
);
const TO_WESTERN = Object.fromEntries(
    [...ARABIC_INDIC_DIGITS].map((digit, index) => [digit, WESTERN_DIGITS[index]])
);

const REGIONAL_RULES = {
    SAR: { symbol: "ر.س", position: "after", thousands: "٬", decimal: "٫" },
    AED: { symbol: "د.إ", position: "after", thousands: "٬", decimal: "٫" },
    MAD: { symbol: "MAD", position: "after", thousands: " ", decimal: "," },
    EGP: { symbol: "ج.م", position: "after", thousands: "٬", decimal: "٫" },
    EUR: { symbol: "€", position: "after", thousands: " ", decimal: "," },
};

function translateDigits(value, table) {
    return String(value ?? "").replace(/[0-9٠-٩]/g, (digit) => table[digit] ?? digit);
}

export function arfrFormatNumerals(value, numeralSystem = "western") {
    if (numeralSystem === "arabic_indic") {
        return translateDigits(value, TO_ARABIC_INDIC);
    }
    if (numeralSystem === "western") {
        return translateDigits(value, TO_WESTERN);
    }
    return String(value ?? "");
}

function currencyName(currency) {
    return String(currency?.name || currency?.code || "").toUpperCase();
}

function currencySymbol(currency, fallback) {
    return currency?.symbol || fallback;
}

function currencyPosition(currency) {
    return currency?.position || "before";
}

function decimalPlaces(currency) {
    return Number.isInteger(currency?.decimal_places) ? currency.decimal_places : 2;
}

function formatNumber(amount, thousands, decimal, digits) {
    const numericAmount = Number(amount || 0);
    const sign = numericAmount < 0 ? "-" : "";
    const fixed = Math.abs(numericAmount).toFixed(digits);
    const [whole, fraction] = fixed.split(".");
    const grouped = whole.replace(/\B(?=(\d{3})+(?!\d))/g, thousands);
    return `${sign}${grouped}${digits ? decimal + fraction : ""}`;
}

export function arfrFormatAmount(amount, currency, preferences = {}) {
    const policy = preferences.currency_format_policy || "odoo_default";
    const name = currencyName(currency);
    const regionalRule = policy === "regional" ? REGIONAL_RULES[name] : null;
    const rule = regionalRule || {
        symbol: currencySymbol(currency, name),
        position: currencyPosition(currency),
        thousands: ",",
        decimal: ".",
    };
    const numeralSystem =
        policy === "force_western" ? "western" : preferences.numeral_system || "western";
    const number = arfrFormatNumerals(
        formatNumber(amount, rule.thousands, rule.decimal, decimalPlaces(currency)),
        numeralSystem
    );

    if (rule.position === "after") {
        return `${number} ${currencySymbol(currency, rule.symbol)}`.trim();
    }
    return `${currencySymbol(currency, rule.symbol)} ${number}`.trim();
}

