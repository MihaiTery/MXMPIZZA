# MXM PIZZA — website preview

Site static în limba română pentru meniul MXM PIZZA. Deschide-l printr-un server static din acest director, de exemplu `python3 -m http.server 3000`, apoi accesează `http://localhost:3000`. `fetch()` pentru `menu.json` cere HTTP, nu deschiderea directă `file://`.

## Conținut și integrare

- `menu.json` conține 73 de poziții: 55 de produse extrase din cele șase documente `.docx` copiate în `source-docs/`, 15 variante de pizza de 50 cm propuse și trei supe cremă cu rețete furnizate de client. `scripts-generate-menu.py` documentează extracția inițială. Editările comerciale viitoare se fac în `menu.json`.
- `price: null` și `available: null` înseamnă informații neconfirmate. Nu publica prețuri sau stocuri fără datele clientului.
- Coșul folosește `localStorage` doar pentru demonstrație. Contul este o interfață fără autentificare. Butonul de finalizare este dezactivat. Integrarea cu platforma de comenzi trebuie să furnizeze prețuri, disponibilitate, autentificare și plasarea reală a comenzilor.
- Adresa și telefonul sunt afișate ca informații în curs de confirmare. Nu există date de contact fictive publicate.
- `assets/logo.jpeg` este logo-ul furnizat de client. `assets/share.svg` este o compoziție originală pentru viitorul preview social; `assets/share.png` este preview-ul social folosit la URL-ul public.

## Handoff BrandForge

`docs/website.manifest.json` este Site Blueprint-ul. `docs/site-assembly.json` păstrează consultarea contractului de componente. Direcția hero și toate verificările rămân **pending**. Implementarea nu a fost verificată vizual, funcțional sau pe dispozitive, conform boundary-ului skill-ului BrandForge. Ownerul va verifica pagina, catalogul, mobilul, tastatura, dialogurile și fluxul demo înainte de publicare.

## Publicare GitHub Pages

Workflow-ul `.github/workflows/pages.yml` publică ramura `main` prin GitHub Actions. În repo, configurează Settings → Pages → Build and deployment → Source: GitHub Actions. Pagina rămâne `noindex` și marcată preview până la confirmarea datelor comerciale.

URL public: https://mihaitery.github.io/MXMPIZZA/

## Hero animat

Logo-ul original este afișat în primul ecran. Pizza este desenată în CSS și reacționează la cursor pe dispozitive cu pointer fin; levitația și aura se opresc în afara ecranului și când fila este ascunsă. `prefers-reduced-motion` păstrează compoziția statică. Direcția rămâne în așteptarea verificării ownerului.

## Logo și WhatsApp

`assets/logo-transparent.webp` este decupajul logo-ului furnizat, folosit în dreapta sus și în footer. `assets/logo.jpeg` păstrează originalul. Widgetul WhatsApp este un mock: sugestiile completează doar mesajul local, nu există număr, link `wa.me` sau trimitere. Verificarea vizuală și funcțională rămâne pending pentru owner.

Butonul coșului este fix în viewport pe mobil și desktop, deasupra widgetului WhatsApp; rămâne demonstrativ, fără checkout real.

Poziția fixă a coșului are fallback CSS explicit pentru browsere desktop care nu acceptă `env(safe-area-inset-bottom)`. Fișierul CSS are versiune în URL pentru actualizarea cache-ului Pages.

## Extinderea meniului

Catalogul are 73 de poziții: 55 extrase din documentele clientului, 15 variante pizza de 50 cm derivate din rețetele de 32 cm și trei supe cremă cu rețete furnizate ulterior de client. Variantele 50 cm nu copiază gramajele de 32 cm; cantitățile și disponibilitatea trebuie confirmate. Supele nu mai sunt marcate mock; prețurile, gramajele și disponibilitatea rămân neconfirmate. Butonul de apel afișează doar `07xx xxx xxx · DEMO` și nu inițiază apeluri.
