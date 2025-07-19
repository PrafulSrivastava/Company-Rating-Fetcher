
// Listen for mouseover on company <a> elements
function isCompanyLink(el) {
  // Generic selector: LinkedIn company links often contain '/company/' in href
  return el.tagName === 'A' && el.href && el.href.includes('/company/');
}

let tooltip = null;

function createTooltip() {
  tooltip = document.createElement('div');
  tooltip.style.position = 'fixed';
  tooltip.style.background = '#222';
  tooltip.style.color = '#fff';
  tooltip.style.padding = '8px 12px';
  tooltip.style.borderRadius = '6px';
  tooltip.style.boxShadow = '0 2px 8px rgba(0,0,0,0.2)';
  tooltip.style.zIndex = 9999;
  tooltip.style.fontSize = '14px';
  tooltip.style.pointerEvents = 'none';
  tooltip.style.transition = 'opacity 0.2s';
  tooltip.style.opacity = '0';
  document.body.appendChild(tooltip);
}

function showTooltip(text, x, y) {
  if (!tooltip) createTooltip();
  tooltip.textContent = text;
  tooltip.style.left = x + 10 + 'px';
  tooltip.style.top = y + 10 + 'px';
  tooltip.style.opacity = '1';
}

function hideTooltip() {
  if (tooltip) {
    tooltip.style.opacity = '0';
    setTimeout(() => {
      if (tooltip) tooltip.remove();
      tooltip = null;
    }, 200);
  }
}

async function fetchRatings(company) {
  try {
    const resp = await fetch(`http://localhost:8000/ratings?company=${encodeURIComponent(company)}`);
    if (!resp.ok) throw new Error('Failed to fetch');
    const data = await resp.json();
    if (Array.isArray(data) && data.length > 0) {
      return data.map(r => `${r.source}: ${r.rating || 'N/A'}`).join(' | ');
    }
    return 'No ratings found.';
  } catch (e) {
    return 'Error fetching ratings.';
  }
}

function extractCompanyNameFromLink(link) {
  // Try to extract company name from URL: /company/{name}/
  const match = link.href.match(/\/company\/([^\/?#]+)/);
  return match ? decodeURIComponent(match[1]) : null;
}

// Event delegation for mouseover/mouseout
let lastTarget = null;
document.addEventListener('mouseover', async (e) => {
  const link = e.target.closest('a');
  if (link && isCompanyLink(link)) {
    lastTarget = link;
    const company = extractCompanyNameFromLink(link);
    if (!company) return;
    showTooltip('Loading ratings...', e.clientX, e.clientY);
    const ratingsText = await fetchRatings(company);
    if (lastTarget === link) {
      showTooltip(ratingsText, e.clientX, e.clientY);
    }
  }
});

document.addEventListener('mousemove', (e) => {
  if (tooltip && tooltip.style.opacity === '1') {
    tooltip.style.left = e.clientX + 10 + 'px';
    tooltip.style.top = e.clientY + 10 + 'px';
  }
});

document.addEventListener('mouseout', (e) => {
  const link = e.target.closest('a');
  if (link && isCompanyLink(link)) {
    lastTarget = null;
    hideTooltip();
  }
});
