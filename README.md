# Floatblue

[![bluebuild build badge](https://github.com/float-labs-devel/floatlabs/actions/workflows/build-daily.yml/badge.svg)](https://github.com/float-labs-devel/floatlabs/actions/workflows/build-daily.yml)

The first image from [Float Labs](https://github.com/float-labs-devel): GNOME on Bluefin DX,
built with [BlueBuild](https://blue-build.org), tracked to Fedora's release cadence,
hardened but not hostile, and written against a 3 to 4 GB machine rather than against
a benchmark.

```sh
sudo bootc switch ghcr.io/float-labs-devel/floatlabs:stable
```

## What it is

A stock GNOME layout — dash to dock and AppIndicator come from Bluefin and are left
alone, because that is how the machine is actually used — with the Flat Remix skin
following light and dark, a hardened system that still lets you work, and a large pile
of the Unix and BSD tools Fedora does not ship by default.

Not a product. One person's image, published because somebody else might want it.

## The three meanings

Float Labs is named for three images, and each has a name and a reason:

* **Floatblue** — GNOME on Bluefin DX. This repo. The one that exists today.
* **Kifloat** — KDE Plasma on Aurora. Not started; it will live in its own repo, because
  a KDE overlay and a GNOME overlay are different work with different upstream.
* **CoreFloat** — headless server on uCore. Not started, also its own repo. A server on
  a ten-year-old box is exactly the case nobody demos, so it is worth doing properly.

All three will share the same foundation modules, so they cannot drift apart.

## Why it exists

The honest reason is a disagreement, not a gap in the market.

A lot of the modern Atomic-desktop scene has been chasing the newest thing that exists
rather than the oldest thing that works. Daily images on KDE BuildStream, on GNOMEOS
nightly, on the FreeDesktop SDK: wonderful for a demo, and a bad foundation for somebody's
daily driver. Alongside it, drivers get dropped on grounds of "modernity" — Broadcom `wl`
being the one that hurts most, because for a 2013 laptop that is the difference between
a desktop and a network-manager error.

Both are defensible. Neither is the only defensible call. This image is the opposite bet:
stock Fedora bases, BlueBuild, Fedora's own release schedule, and the drivers kept.

None of this is a criticism of the people who maintain those images. Most of them are
volunteers too, and the work they do is genuinely hard. It is a difference of opinion
about what the default should be.

## Where the low-end target comes from

The reference machine is a 3 to 4 GB laptop with a Sandy Bridge i5-3550. No AVX2, and an
integrated GPU from before Vulkan existed in Mesa. Every low-end decision follows from
those two facts:

* **No Vulkan anywhere.** A pre-Haswell iGPU has no Vulkan driver, so anything built
  around it either refuses to start or falls back to software Vulkan and ends up slower
  than the OpenGL path it replaced. Gamescope and MangoHud are deliberately absent. On a
  GPU from Haswell on, install both — this is the one place performance is knowingly left
  on the table.
* **zram, half of RAM and never over 2 GB**, with `vm.swappiness` raised to 180. Being
  reluctant to use swap that lives in compressed RAM just wastes memory.
* **earlyoom** instead of the kernel OOM killer, which kills the biggest process and says
  which one instead of picking at random and leaving you at a black screen.
* **`tracker-miners-fs3`, PackageKit, `man-db` and `plocate` off.** Idle most of the time,
  resident all of the time. A poor trade on 4 GB.
* **Shell animations off, system-wide.** Every window open is a full screen repaint on a
  weak GPU.

## Hardening, and what was taken back out

The hardening starts from [secureblue](https://github.com/secureblue/secureblue), which is
the best reference for this kind of work, and then takes a good deal of it back out again.
The reason is simple: this has to be a daily driver, and there is an i5-3550 under the desk
that must not be made slower.

Kept: a large set of kernel and network sysctls, core dumps off everywhere, `pam_faillock`
and `pam_pwquality`, per-network MAC randomisation, NTS time sync, its own firewalld zone,
`geoclue` and `passim` masked, and doas alongside sudo.

Taken back out:

* **sudo, su and pkexec all stay.** Replacing them with `run0` starts a whole systemd
  session every time you call it, and it breaks ordinary scripting.
* **Xwayland stays on**, the image has Steam. **ping stays on**, the image has a network
  toolset. **`perf_event_paranoid` is 2, not 3**, so perf still works on your own processes.
* **`rp_filter` is loose, not strict.** Strict drops legitimate packets on a laptop with
  Wi-Fi, Ethernet and a VPN at once, which shows up as "the internet randomly doesn't work".
* **No blanket module blacklisting.** `squashfs` is load-bearing for ostree, bootc and the
  ISO build.
* **No restrictive `containers/policy.json`.** podman and `bootc switch` are how this image
  installs and updates itself.
* **The dock stays, the blur does not.** Blur My Shell is disabled through the system dconf
  database.

usbguard is installed but not enabled, and AIDE's database is not built at image build
time: a policy that blocks the wrong USB class takes your keyboard with it, and
`aideinit` would add minutes to every build. Run `sudo aideinit` once.

## Gaming

GameMode runs on demand — governor up, game re-niced, everything put back when it exits.
Two sysctls from the hardening set genuinely block games and the gaming profile relaxes
both, which is a real trade worth writing down rather than hiding:

* `kernel.io_uring_disabled` goes from 2 to 1. Off on the grounds of a long history of
  kernel bugs, which is fair, but Wine and Proton use it for ordinary file I/O. 1 keeps the
  syscall behind a permission check instead of removing it.
* `vm.mmap_rnd_bits` goes from 32 back to 28, the upstream default. 32 leaves too little
  address space for the very large reservations DXVK makes.

kexec, BPF, userfaultfd, `tcp_timestamps` and the ASLR setting itself are never touched,
and `apply-gaming-tuning.sh` fails the build if a typo in the drop-in takes one of them
down with it.

## Channels

| Channel | Base channel | What it means |
|---|---|---|
| `gts` | `gts` | Fedora's ground-to-shoot. The most conservative thing here. |
| `stable` | `stable` | **Recommended.** A week of soak before it moves. |
| `latest` | `latest` | The daily canary, and the first thing that will break. |

Each carries the Fedora version it was built against, read out of the image itself rather
than out of this repository.

## Building it

```sh
bluebuild build --build-driver=podman recipes/floatblue-stable.yml
```

Builds run on GitHub Actions daily (`latest`) and weekly (`stable`, `gts`).

## Layout

```
recipes/                  one file per channel, three channels
recipes/features/         the overlay, composed from modules
recipes/features/shared-foundation.yml   what all three images get
recipes/features/gnome/    what only Floatblue gets
files/scripts/            the tuning and hardening scripts
files/system/             sysctls, firewall, chrony, audit rules
installer/                titanoboa live ISO, installs to disk
website/                  the site
```

Every script fails the build rather than guessing. Dropping a keyfile into
`/etc/dconf/db/distro.d` does nothing without a `dconf update`, so `apply-desktop-dconf.sh`
runs it and reads the result back; a profile that compiled but did not take effect fails
the build instead of silently doing nothing. User Themes goes into the *system* extension
list, not the user one, because the shell reads its extension list before
`float-theme-sync` gets a chance to run.

## No money

Float Labs takes no money. No sponsors, no tiers, no company, no "professional" edition.
It is one person with weaker hardware who is unsatisfied with a direction upstream. That
is the whole funding model.

## Licence

Apache-2.0, inherited from the floatblue image this grew out of. It builds on Bluefin and
BlueBuild; those are theirs, under their own licences.