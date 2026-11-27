# MXM PIZZA — website preview

Site static în limba română pentru meniul MXM PIZZA. Deschide-l printr-un server static din acest director, de exemplu `python3 -m http.server 3000`, apoi accesează `http://localhost:3000`. `fetch()` pentru `menu.json` cere HTTP, nu deschiderea directă `file://`.

## Conținut și integrare

- `menu.json` conține toate cele 55 de produse extrase din cele șase documente `.docx` copiate în `source-docs/`. `scripts-generate-menu.py` documentează extracția inițială. Editările comerciale viitoare se fac în `menu.json`.
- `price: null` și `available: null` înseamnă informații neconfirmate. Nu publica prețuri sau stocuri fără datele clientului.
- Coșul folosește `localStorage` doar pentru demonstrație. Contul este o interfață fără autentificare. Butonul de finalizare este dezactivat. Integrarea cu platforma de comenzi trebuie să furnizeze prețuri, disponibilitate, autentificare și plasarea reală a comenzilor.
- Adresa și telefonul sunt afișate ca informații în curs de confirmare. Nu există date de contact fictive publicate.
- `assets/logo.jpeg` este logo-ul furnizat de client. `assets/share.svg` este o compoziție originală pentru viitorul preview social; adaugă un URL HTTPS absolut în metadate după stabilirea domeniului.

## Handoff BrandForge

`docs/website.manifest.json` este Site Blueprint-ul. `docs/site-assembly.json` păstrează consultarea contractului de componente. Direcția hero și toate verificările rămân **pending**. Implementarea nu a fost verificată vizual, funcțional sau pe dispozitive, conform boundary-ului skill-ului BrandForge. Ownerul va verifica pagina, catalogul, mobilul, tastatura, dialogurile și fluxul demo înainte de publicare.

## Publicare GitHub Pages

Workflow-ul `.github/workflows/pages.yml` publică ramura `main` prin GitHub Actions. În repo, configurează Settings → Pages → Build and deployment → Source: GitHub Actions. Pagina rămâne `noindex` și marcată preview până la confirmarea datelor comerciale.
