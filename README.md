# siguelo_turnstile_solver

A Python executable module that automates [`Siguelo Plus`](https://siguelo.sunarp.gob.pe/siguelo/) queries,
handling the Cloudflare Turnstile CAPTCHA with the help of [`2Captcha`](https://pypi.org/project/2captcha-python/) service.
This library is built on top of the [`playwright`](https://pypi.org/project/playwright/) library.

---

⚠️ **Disclaimer**

This project is an **independent, personal tool** created for convenience.
It is **not affiliated with, endorsed by, or connected to** the administrators, owners, or developers of the target platform.

- The module does **not replace, modify, or bypass** any proprietary software or service.
- It only automates **my own manual queries** to avoid the repetitive task of checking titles one by one.
- It requires a valid [2Captcha](https://2captcha.com) account to solve CAPTCHA challenges.

I am not responsible for how others may use this code. Each user is solely accountable for complying with the **laws, terms of service, and conditions** of the platform involved.

If the owners or relevant authorities raise any concerns, I am fully willing to **collaborate, modify, or remove** this project.

---

## Purpose

The purpose of this project is **personal use only**:

- Automating repetitive access to “Síguelo” to check my own titles.
- Avoiding manual solving of Cloudflare Turnstile CAPTCHA.

This project is **not intended** to:

- Replace official authentication or validation processes.
- Circumvent payment, restrictions, or legal requirements of Sunarp.
- Be used for unauthorized access or third-party services.

---

## Important Notice on Terms of Service

According to the official [Términos y Condiciones de “Síguelo Plus”](https://sigueloplus.sunarp.gob.pe/siguelo/), access to the platform is subject to:

- **Time-limited access** to certain documents.
- **Strict limitations on usage** (no misuse, no providing access to third parties, no overloading the system).
- **Prohibition of use with illicit purposes** or against Sunarp’s guidelines.

This module does **not attempt to override or ignore** any of these conditions.
Users are fully responsible for ensuring their use of this project complies with:

- The **Términos y Condiciones de “Síguelo Plus”**.
- Applicable laws and regulations.

The author assumes **no liability** for misuse or damages caused by the use of this project.

---

## Installation

Clone this repository directly:

```bash
git clone https://github.com/CesarZHX/siguelo_turnstile_solver.git
cd siguelo_turnstile_solver
```

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # On Linux/Mac
.venv\Scripts\activate      # On Windows

pip install -r requirements.txt
```

---

## Responsible Use

- Use at your own risk.
- You are solely responsible for compliance with **third-party terms, laws, and policies**.
- The author accepts **no liability** for misuse, damages, or legal issues.

---

## License

This project is released under the [Apache License 2.0](./LICENSE).
You are free to use, modify, and distribute it under the conditions of that license.
See the LICENSE file for details.
