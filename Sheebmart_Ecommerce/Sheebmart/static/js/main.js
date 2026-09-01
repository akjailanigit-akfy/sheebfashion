(function () {
    const csrfToken = document.cookie.split("; ").find(row => row.startsWith("csrftoken="))?.split("=")[1];

    function updateCount(count) {
        const badge = document.getElementById("cartCount");
        if (badge) badge.textContent = count;
    }

    function readLocalCart() {
        try { return JSON.parse(localStorage.getItem("sheebmart_cart") || "{}"); }
        catch { return {}; }
    }

    function writeLocalCart(cart) {
        localStorage.setItem("sheebmart_cart", JSON.stringify(cart));
        localStorage.setItem("sheebmart_cart_updated", Date.now().toString());
    }

    async function addToCart(button) {
        const productId = button.dataset.productId;
        const qtySource = button.dataset.quantitySource;
        const quantity = Number(qtySource ? document.getElementById(qtySource)?.value || 1 : 1);
        const url = window.SHEEBMART.addToCartUrlTemplate.replace("__ID__", productId);

        // Retrieve selected options from sessionStorage
        const optionsData = sessionStorage.getItem(`product_options_${productId}`);
        const options = optionsData ? JSON.parse(optionsData) : { size: null, color: null };
        
        // Create display text for selected options
        const optionsText = [];
        if (options.size) optionsText.push(`Size: ${options.size}`);
        if (options.color) optionsText.push(`Color: ${options.color}`);
        const optionsDisplay = optionsText.length > 0 ? ` (${optionsText.join(', ')})` : '';

        button.disabled = true;
        const oldText = button.innerHTML;
        button.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken || "",
                    "X-Requested-With": "XMLHttpRequest",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({ quantity, options: JSON.stringify(options) }),
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.message || "Unable to add to cart.");
            updateCount(data.count);
            const localCart = readLocalCart();
            localCart[productId] = (Number(localCart[productId]) || 0) + quantity;
            writeLocalCart(localCart);
            showToast(data.message + optionsDisplay);
        } catch (error) {
            showToast(error.message, true);
        } finally {
            button.disabled = false;
            button.innerHTML = oldText;
        }
    }

    function showToast(message, error = false) {
        const toast = document.createElement("div");
        toast.className = "position-fixed bottom-0 end-0 m-3 px-4 py-3 rounded-3 shadow text-white";
        toast.style.zIndex = "9999";
        toast.style.background = error ? "#8a1c25" : "#111";
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 2500);
    }

    document.querySelectorAll(".add-cart-btn").forEach(button => {
        button.addEventListener("click", () => addToCart(button));
    });

    document.querySelectorAll(".buy-now-btn").forEach(button => {
        button.addEventListener("click", async () => {
            const productId = button.dataset.productId;
            const qtySource = button.dataset.quantitySource;
            const quantity = Number(qtySource ? document.getElementById(qtySource)?.value || 1 : 1);
            const url = window.SHEEBMART.addToCartUrlTemplate.replace("__ID__", productId);
            
            // Retrieve selected options from sessionStorage
            const optionsData = sessionStorage.getItem(`product_options_${productId}`);
            const options = optionsData ? JSON.parse(optionsData) : { size: null, color: null };
            
            button.disabled = true;
            try {
                const response = await fetch(url, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken || "",
                        "X-Requested-With": "XMLHttpRequest",
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    body: new URLSearchParams({ quantity, options: JSON.stringify(options) }),
                });
                const data = await response.json();
                if (!response.ok) throw new Error(data.message || "Unable to continue.");
                updateCount(data.count);
                const localCart = readLocalCart();
                localCart[productId] = (Number(localCart[productId]) || 0) + quantity;
                writeLocalCart(localCart);
                window.location.href = "/cart/checkout/";
            } catch (error) {
                showToast(error.message, true);
                button.disabled = false;
            }
        });
    });

    window.addEventListener("storage", () => window.location.reload());
})();
