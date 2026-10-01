# Float Labs contributors

## The short version

There is one of us, and there is no money involved.

Float Labs is not a company, a foundation, or a project with a board and a budget. It is
one person — [floatingskies](https://github.com/floatingskies) — with an older laptop
under a desk and a disagreement with a direction upstream about what an Atomic desktop
should be built on. No funding, no sponsors, no paid tiers, no support contracts. Builds
run on GitHub Actions. If it stops, it stops.

That is worth saying plainly at the top rather than discovering later. Nobody should read
this organisation and expect a vendor behind it.

## Who

| Who | Role |
|---|---|
| [@floatingskies](https://github.com/floatingskies) | Maintainer. Recipes, scripts, builds, the arguments, the old hardware. |

That table will stay short for a while. If it grows, it grows because somebody sent a fix
that worked, not because anybody was appointed.

## What actually helps

Hardware reports are the most valuable thing and the scarcest. "This image does not come
up on my ThinkPad T430 with Broadcom" is worth more here than any other kind of report,
because the entire reason this exists is that other images dropped that case. A report
that says "it works, here is the model and the wireless chip" is just as useful.

After that:

* **Fixes, with the failure written down.** Not just the patch — what broke, on what, and
  what you expected instead. That is the part that is impossible to reconstruct later.
* **Disagreement in an issue.** If the reasoning is written out, it can be argued with. If
  it is only a vote or a reaction, it cannot.
* **Tests on real machines.** Especially old ones. Especially the ones nobody tests.

## What does not help

* Money. There is nothing to buy and nothing to sell. Please do not offer.
* Feature requests for hardware this project does not target. It targets 3 to 4 GB machines
  with pre-Haswell integrated graphics. A request for something that assumes a discrete GPU
  is a request for a different project.
* Patches that add dependencies. Every package added is a package that has to survive
  the next Fedora release, and the overlay is kept deliberately flat.
* Divergence from stock Fedora. If it needs a third-party repository and nobody can say why
  an upstream package will not do, it probably does not belong in the image.
* Patches against an untested upstream base. Building a daily image on KDE BuildStream,
  GNOMEOS nightly or the FreeDesktop SDK is the thing this project exists as an argument
  against. Do not bring that argument into the build.

## How to contribute

Everything is in the open under Apache-2.0. Open an issue describing your hardware and
what happened, or send a pull request against the relevant recipe or script. Every script
in `files/scripts/` is written to fail the build rather than guess, so if you find a case
where one silently succeeds when it should not, that is a real bug and worth reporting.

There is no CLA, no contributor licence agreement, and no code of conduct document,
because there is no organisation here that needs one yet. Be reasonable to each other.

## Naming, if you are reading this to judge the project

Three images, three names, one meaning each:

* **Floatblue** — GNOME on Bluefin DX.
* **Kifloat** — KDE Plasma on Aurora.
* **CoreFloat** — headless server on uCore.

Same foundation, same hardening, same low-end target, Fedora's own release cadence. The
first one exists. The other two are on the way and will get their own repositories.