const categories={all:'Tot meniul',pizza:'Pizza 32 cm',pizza50:'Pizza 50 cm',shaorma:'Shaorma & kebab',meniu:'Meniuri & schnitzel',paste:'Paste',salate:'Salate',supe:'Supe cremă',deserturi:'Deserturi',bauturi:'Băuturi'};
const state={items:[],category:'all',search:'',cart:readCart()};
const grid=document.querySelector('#menuGrid');
const filters=document.querySelector('#categoryFilters');
const count=document.querySelector('#resultCount');
function readCart(){try{return JSON.parse(localStorage.getItem('mxm-demo-cart')||'{}')}catch{return {}}}
function saveCart(){localStorage.setItem('mxm-demo-cart',JSON.stringify(state.cart));renderCart()}
function safe(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function renderFilters(){const left=filters.scrollLeft;filters.innerHTML=Object.entries(categories).map(([key,label])=>`<button type="button" data-category="${key}" aria-pressed="${state.category===key}">${label}</button>`).join('');filters.scrollLeft=left;requestAnimationFrame(updateCategoryArrows)}
function renderMenu(){const q=state.search.toLocaleLowerCase('ro').trim();const shown=state.items.filter(item=>(state.category==='all'||item.category===state.category)&&(!q||`${item.name} ${item.description}`.toLocaleLowerCase('ro').includes(q)));count.textContent=`${shown.length} ${shown.length===1?'produs':'produse'} afișate`;grid.innerHTML=shown.length?shown.map((item,index)=>`<article class="product-card"><div class="product-top"><div class="product-labels"><span class="product-category">${safe(categories[item.category])}</span>${item.badge?`<span class="product-badge">${safe(item.badge)}</span>`:''}</div><span class="product-index">${String(index+1).padStart(2,'0')}</span></div><h3>${safe(item.name)}</h3><p>${safe(item.description||'Detalii în curs de confirmare.')}</p><div class="product-bottom"><span class="price-pending">Preț în curând</span><button class="add-button" type="button" data-add="${item.id}" aria-label="Adaugă ${safe(item.name)} în coșul demonstrativ">+ Coș demo</button></div></article>`).join(''):'<p class="empty-results">Nu am găsit produse pentru această căutare.</p>'}
function renderCart(){const entries=Object.entries(state.cart).filter(([,qty])=>qty>0);const total=entries.reduce((n,[,qty])=>n+qty,0);document.querySelector('#cartCount').textContent=total;document.querySelector('#cartItems').innerHTML=entries.length?entries.map(([id,qty])=>{const item=state.items.find(x=>x.id===id);if(!item)return '';return `<div class="cart-row"><div><strong>${safe(item.name)}</strong><small>Preț în curs de confirmare</small></div><div class="qty"><button type="button" data-qty="${id}" data-delta="-1" aria-label="Scade cantitatea pentru ${safe(item.name)}">−</button><span>${qty}</span><button type="button" data-qty="${id}" data-delta="1" aria-label="Crește cantitatea pentru ${safe(item.name)}">+</button></div></div>`}).join(''):'<p class="empty-results">Coșul este gol. Alege ceva bun din meniu.</p>';document.querySelector('#cartSummary').textContent=`${total} ${total===1?'produs':'produse'} · Total indisponibil până la publicarea prețurilor.`}
filters.addEventListener('click',e=>{const b=e.target.closest('[data-category]');if(!b)return;state.category=b.dataset.category;renderFilters();renderMenu();filters.querySelector(`[data-category="${state.category}"]`)?.scrollIntoView({block:'nearest',inline:'center',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})});
document.querySelector('#menuSearch').addEventListener('input',e=>{state.search=e.target.value;renderMenu()});
grid.addEventListener('click',e=>{const b=e.target.closest('[data-add]');if(!b)return;state.cart[b.dataset.add]=(state.cart[b.dataset.add]||0)+1;saveCart();b.textContent='Adăugat ✓';setTimeout(()=>b.textContent='+ Coș demo',900)});
document.querySelector('#cartItems').addEventListener('click',e=>{const b=e.target.closest('[data-qty]');if(!b)return;const id=b.dataset.qty;state.cart[id]=Math.max(0,(state.cart[id]||0)+Number(b.dataset.delta));if(!state.cart[id])delete state.cart[id];saveCart()});
document.querySelector('#cartButton').addEventListener('click',()=>document.querySelector('#cartDialog').showModal());
document.querySelector('#accountButton').addEventListener('click',()=>document.querySelector('#accountDialog').showModal());
document.querySelectorAll('[data-close]').forEach(b=>b.addEventListener('click',()=>document.getElementById(b.dataset.close).close()));
document.querySelectorAll('dialog').forEach(d=>d.addEventListener('click',e=>{if(e.target===d)d.close()}));
fetch('menu.json?v=copy-audit-2').then(r=>r.json()).then(items=>{state.items=items;renderFilters();renderMenu();renderCart()}).catch(()=>{grid.innerHTML='<p class="empty-results">Meniul nu s-a putut încărca. Reîncarcă pagina.</p>'});

// Pointer motion stays on the decorative pizza; text and controls remain still.
(()=>{
 const hero=document.querySelector('.hero');
 const art=document.querySelector('.hero-art');
 if(!hero||!art)return;
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const fine=matchMedia('(hover: hover) and (pointer: fine)');
 let visible=true,frame=0,targetX=0,targetY=0;
 const reset=()=>{targetX=targetY=0;art.style.setProperty('--move-x','0px');art.style.setProperty('--move-y','0px');art.style.setProperty('--tilt-x','0deg');art.style.setProperty('--tilt-y','0deg')};
 const update=()=>{frame=0;if(!visible||reduced.matches||!fine.matches)return reset();art.style.setProperty('--move-x',`${(targetX*24).toFixed(1)}px`);art.style.setProperty('--move-y',`${(targetY*20).toFixed(1)}px`);art.style.setProperty('--tilt-x',`${(-targetY*9).toFixed(1)}deg`);art.style.setProperty('--tilt-y',`${(targetX*9).toFixed(1)}deg`)};
 art.addEventListener('pointermove',e=>{if(!visible||reduced.matches||!fine.matches)return;const r=art.getBoundingClientRect();targetX=Math.max(-1,Math.min(1,((e.clientX-r.left)/r.width-.5)*2));targetY=Math.max(-1,Math.min(1,((e.clientY-r.top)/r.height-.5)*2));if(!frame)frame=requestAnimationFrame(update)});
 art.addEventListener('pointerleave',reset);
 const observer=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting&&!document.hidden;hero.dataset.artActive=String(visible);if(!visible)reset()},{threshold:0});observer.observe(hero);
 document.addEventListener('visibilitychange',()=>{visible=!document.hidden&&hero.getBoundingClientRect().bottom>0&&hero.getBoundingClientRect().top<innerHeight;hero.dataset.artActive=String(visible);if(!visible)reset()});
 reduced.addEventListener('change',()=>{if(reduced.matches)reset()});
})();

// WhatsApp preview: local draft only; no number, network request, or send action.
(()=>{
 const button=document.querySelector('#whatsappButton');
 const dialog=document.querySelector('#whatsappDialog');
 const draft=document.querySelector('#waDraft');
 if(!button||!dialog||!draft)return;
 button.addEventListener('click',()=>dialog.showModal());
 dialog.querySelectorAll('[data-wa-message]').forEach(choice=>choice.addEventListener('click',()=>{draft.value=choice.dataset.waMessage;draft.focus()}));
})();

// Category arrows remain visible while the list can scroll horizontally.
const categoryPrev=document.querySelector('#categoryPrev');
const categoryNext=document.querySelector('#categoryNext');
function updateCategoryArrows(){const max=filters.scrollWidth-filters.clientWidth;categoryPrev.disabled=filters.scrollLeft<2;categoryNext.disabled=filters.scrollLeft>max-2||max<2}
categoryPrev.addEventListener('click',()=>filters.scrollBy({left:-Math.max(220,filters.clientWidth*.65),behavior:'smooth'}));
categoryNext.addEventListener('click',()=>filters.scrollBy({left:Math.max(220,filters.clientWidth*.65),behavior:'smooth'}));
filters.addEventListener('scroll',updateCategoryArrows,{passive:true});
window.addEventListener('resize',updateCategoryArrows);
requestAnimationFrame(updateCategoryArrows);

// Call is a local preview until the client supplies a real phone number.
document.querySelectorAll('.call-trigger').forEach(button=>button.addEventListener('click',()=>document.querySelector('#callDialog').showModal()));

// Pause the category marquee outside the viewport or when the tab is hidden.
(()=>{
 const ticker=document.querySelector('.ticker');
 if(!ticker)return;
 let inView=false;
 const sync=()=>{ticker.dataset.visible=String(inView&&!document.hidden)};
 const observer=new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;sync()},{threshold:0});
 observer.observe(ticker);
 document.addEventListener('visibilitychange',sync);
})();
