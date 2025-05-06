// Enhanced Search Engine JavaScript
$(document).ready(function () {
    // Add search page class to body if results are present
    const hasResults = $('.results-container').length > 0 || $('table tbody tr').length > 0;
    if (hasResults || $('input[name="query"]').val().trim() !== '') {
        $('body').addClass('search-results');
    }

    // Add animation classes to search results
    $('tbody tr').each(function (index) {
        $(this).css('animation-delay', (0.1 + index * 0.05) + 's');
        $(this).addClass('animated-row');
    });

    // Add loading effect when form is submitted
    $('form').on('submit', function () {
        if ($('input[name="query"]').val().trim() !== '') {
            showLoading();
        }
    });

    // Format URL display by truncating and adding tooltips
    $('.table a').each(function () {
        const fullUrl = $(this).text();

        // Extract domain for display
        let displayUrl = fullUrl;
        try {
            const urlObj = new URL(fullUrl);
            const pathLength = urlObj.pathname.length > 20 ?
                urlObj.pathname.substring(0, 17) + '...' :
                urlObj.pathname;
            displayUrl = urlObj.hostname + pathLength;
        } catch (e) {
            // If URL parsing fails, use original text
        }

        // Set tooltip with full URL
        $(this).attr('title', fullUrl);
        $(this).data('toggle', 'tooltip');

        // Replace text with shortened version if needed
        if (fullUrl.length > 40) {
            $(this).text(displayUrl);
        }
    });

    // Initialize tooltips
    $('[data-toggle="tooltip"]').tooltip();

    // Add frequency and rank styling
    $('.table tr').each(function () {
        const $cells = $(this).find('td');
        if ($cells.length >= 3) {
            // Format frequency cell
            if ($(this).closest('table').find('th:contains("Frequency")').length) {
                const $freqCell = $cells.eq(2);
                const freq = parseInt($freqCell.text());
                $freqCell.html(`<span class="frequency-badge">${freq}</span>`);
            }

            // Format PageRank cell
            if ($(this).closest('table').find('th:contains("PageRank")').length) {
                const $rankCell = $cells.eq(2);
                const rank = parseFloat($rankCell.text());
                $rankCell.html(`<span class="pagerank-badge">${rank.toFixed(6)}</span>`);
            }
        }
    });

    // Add word highlight effect
    $('.table td:nth-child(2)').each(function () {
        const word = $(this).text();
        $(this).html(`<span class="highlight-word">${word}</span>`);
    });

    // Add table row hover effect
    $('.table tbody tr').hover(
        function () {
            $(this).addClass('table-active');
        },
        function () {
            $(this).removeClass('table-active');
        }
    );

    // Add click animation to search button
    $('.search-button').on('mousedown', function () {
        $(this).addClass('btn-active');
    }).on('mouseup mouseleave', function () {
        $(this).removeClass('btn-active');
    });

    // Keyboard shortcut for search focus (press / key)
    $(document).on('keydown', function (e) {
        if (e.key === '/' && !$(e.target).is('input, textarea')) {
            e.preventDefault();
            $('input[name="query"]').trigger('focus');
        }
    });
});

// Show loading indicator
function showLoading() {
    // Create loading overlay if not exists
    if ($('#loading-overlay').length === 0) {
        const loadingHtml = `
            <div id="loading-overlay" class="position-fixed top-0 left-0 w-100 h-100 d-flex justify-content-center align-items-center bg-white" style="z-index: 1050; opacity: 0.9;">
                <div class="text-center">
                    <div class="spinner-border mb-3" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <h5 class="mt-2 text-primary">Searching...</h5>
                </div>
            </div>
        `;
        $('body').append(loadingHtml);
    }

    $('#loading-overlay').fadeIn(200);
}

// Hide loading indicator (called when page is fully loaded)
$(window).on('load', function () {
    $('#loading-overlay').fadeOut(200, function () {
        $(this).remove();
    });
});