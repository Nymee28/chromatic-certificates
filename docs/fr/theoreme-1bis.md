# Théorème 1 bis — La présentation finie de G_CH(q,4) en module 4
### Pièce d'assemblage : énoncé, preuve par composition, table des faits machine, statut de chaque maillon

*Dossier 9, pièce finale du jalon J2. 28 juillet 2026. Convention de statuts du recueil : [T-ℚ] démontré exact sur ℚ ; [C-p] computationnel modulo premiers concordants ; [L] lemme rédigé, liste [R] ouverte ; [CONJ] conjecture. Pièces sœurs : `lemme-C-mod4.md` (la fermeture), `le-concept.md` § 5.2 (le journal des quatre passes), bilans CC-01/CC-02 (les faits machine).*

---

## 1. L'énoncé

> **Théorème 1 bis.** Soit G_CH(q,4) le graphe circulant de Cameron–Hoàng d'ordre n = 4q+1 (5-sommet-critique, non-4-coloriable), q ≥ 3. Alors :
>
> **(i)** *(certificats)* G_CH(q,4) admet un certificat de Nullstellensatz exact sur ℚ de non-4-coloriabilité, de degré 5 (encodage racines quartiques, niveaux {1, 5}), supporté sur les arêtes d'écart ≤ 3 = k−1, de forme éclaireur × gadget (rayon L = 3, un éclaireur).
>
> **(ii)** *(présentation)* La famille entière est capturée par un objet fini : un alphabet de **6 487 étiquettes** indépendantes de n (écart, motif de gadget, exposant d'éclaireur, résidu de position mod 4, signe), un ensemble d'équations fermé (**6 186** équations pour q ≥ 10), et **deux vecteurs de constantes rationnelles** V_pair et V_impair (411 et 401 coefficients actifs, dénominateurs divisant 16 = 2⁴) tels que, pour q ≥ 6, le certificat de G_CH(q,4) est l'instanciation de V_{q mod 2}.
>
> **(iii)** *(strates)* La 2-périodicité en q est causée par l'arithmétique antipodale : ⌊n/2⌋ = 2q ≡ 0 ou 2 (mod 4) selon la parité de q — les deux strates sont l'ombre de n mod 8 ∈ {1, 5}.

## 2. La preuve, par composition de maillons

**Maillon 1 — petits ordres (q = 3, 4, 5).** Certificats exacts individuels, solutions des systèmes d'étiquettes propres, vérification A·μ = e sur ℚ jusqu'à l'étage des colonnes (334 394 lignes à q = 6 pour la plus grande vérification descendue). Statut : **[T-ℚ]**. *(Sources : `j2_labels_q3/4/5.json`, `j2_verify_joint.py` 4/4 OK, reproduction inter-machines bit à bit CC-01 § 3.2.)*

**Maillon 2 — le régime périodique observé (q = 6…12).** Sept ordres consécutifs : les solves exacts indépendants redonnent V_pair (q = 6, 8, 10, 12) et V_impair (q = 7, 9, 11) **bit à bit** ; les évaluations directes donnent PREDICTION OK (0 équation violée sur 6 186) à q = 10, 11, 12 ; test de discrimination calibré (un coefficient perturbé de +1 → ÉCHEC détecté, CC-02 § 3.1). Statut : **[T-ℚ]** sur chacun des sept ordres. *(Sources : CC-01 § 3.4, CC-02 § 3.2-3.5.)*

**Maillon 3 — la fermeture des équations.** (a) *Empirique* : alphabet constant depuis q = 5 ; série des incréments d'équations 1299, 1384, 947, 317, 63, 12, 2, **0, 0** — nul à q = 11 et q = 12, deux pas consécutifs (CC-02 § 1c). (b) *Structurel* : le Lemme C-mod4 (`lemme-C-mod4.md`) — fenêtres de largeur ≤ 10 (Lemme F), saturation des types (Lemme S, n ≥ 25), invariance de signature dans la zone générique de l'éclaireur par pas de 4 (Lemme Z), catalogue de bord antipodal fonction de q mod 2 seul (Lemme B), d'où 𝔈_q = 𝔈_{q mod 2} pour q ≥ q₀ = 10. Statut : **[L]**, liste [R] ci-dessous. *(La valeur q₀ = 10 est celle que les données imposent — les incréments +14/+2 au-delà de q = 8 étaient des réalisations tardives, R2 tranché.)*

**Maillon 4 — l'instanciation.** Pour q ≥ 10 : 𝔈_q = 𝔈_{q mod 2} (maillon 3) ; V_{q mod 2} ⊨ 𝔈_{q mod 2} (maillon 2, q = 10, 11, 12) ; donc V_{q mod 2} satisfait le système d'étiquettes de G_CH(q,4) ; la redistribution des constantes sur les colonnes (chaque colonne reçoit la valeur de son étiquette) satisfait chaque ligne du système restreint — c'est la construction même du quotient, validée numériquement quatre fois à l'étage des colonnes (maillon 1). Le certificat exact existe à tout q ≥ 10. Avec les maillons 1-2 (q = 3…12), la famille est couverte en entier. ∎ *(modulo [R])*

## 3. La table des douze ordres

| q | n | équations | incrément | étiquettes | LCM dén. | actives | identité à V_{q mod 2} | statut |
|---|---|---|---|---|---|---|---|---|
| 3 | 13 | 2 162 | — | 3 853 | 48 | 390 | (pré-période) | [T-ℚ] |
| 4 | 17 | 3 461 | +1 299 | 5 827 | 48 | 757 | (pré-période) | [T-ℚ] |
| 5 | 21 | 4 845 | +1 384 | 6 487 | 16 | 431 | (pré-période) | [T-ℚ] |
| 6 | 25 | 5 792 | +947 | 6 487 | 16 | 411 | OUI | [T-ℚ] |
| 7 | 29 | 6 109 | +317 | 6 487 | 16 | 401 | OUI | [T-ℚ] |
| 8 | 33 | 6 172 | +63 | 6 487 | 16 | 411 | OUI | [T-ℚ] |
| 9 | 37 | 6 184 | +12 | 6 487 | 16 | 401 | OUI | [T-ℚ] |
| 10 | 41 | 6 186 | +2 | 6 487 | 16 | 411 | OUI + prédiction | [T-ℚ] |
| 11 | 45 | **6 186** | **0** | 6 487 | 16 | 401 | OUI + prédiction | [T-ℚ] |
| 12 | 49 | **6 186** | **0** | 6 487 | 16 | 411 | OUI + prédiction | [T-ℚ] |

Bonus consigné sans exploitation : V_impair satisfait aussi le système de q = 3 (sous-déterminé) — la présentation déborde vers le bas.

## 4. Ce que le théorème apporte au programme

1. **Deuxième famille entièrement capturée, premier transport inter-modules.** Le concept de présentation finie (dossier 9) n'est plus un constat sur un pilier : c'est une méthode qui a traversé un changement d'anneau (x³ = 1 → x⁴ = 1), avec des lois qui se répondent — écart minimal k−1 (2 puis 3), dénominateurs (2·3² puis 2⁴), strates de parité (mécanisme prouvé ici, découvert péniblement là), grammaire éclaireur×gadget identique.
2. **La loi des constantes la plus simple des trois piliers** : aucune dépendance en n — deux vecteurs purs. Le pilier 1 avait des échelles en n et des clés de zone ; ZJ avait ν = n·μ et ses strates ; le module 4 n'a que la parité.
3. **La matière première de la règle de construction** (bascule 2 de la doctrine) : trois familles, trois certificats exacts explicites, un vocabulaire commun — le terrain du chantier d'invention « extraire la règle » est prêt.

## 5. Liste [R] consolidée (état au 28 juillet)

- **R1** (motifs fusionnés, mécanique) → confié à CC-03, mission D.
- **R2** (l'incrément +12 de q=9) → **TRANCHÉ** : réalisations tardives, q₀ = 10, deux incréments nuls consécutifs (CC-02).
- **R3** (réalisation effective des types du catalogue) → mécanique, non urgent : la fermeture empirique (deux zéros) couvre le besoin en attendant.
- **R4** (rédaction formelle de la composition quotient/colonnes) → à faire au moment de la mise au propre pour soumission ; validée numériquement 4×.
- **R5** (jauge V_pair/V_impair : une strate à équivalence près ?) → confié à CC-03, mission C ; le verdict précisera l'énoncé (ii) sans le fragiliser.
