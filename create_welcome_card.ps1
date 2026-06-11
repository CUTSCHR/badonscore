Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms

$ErrorActionPreference = 'Stop'
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$outPath = Join-Path $scriptDir 'welcome_card.png'
$logoPath = Join-Path $scriptDir 'logo.png'

$W = 1800
$H = 2400
$cream = [System.Drawing.Color]::FromArgb(245, 240, 232)
$deepGreen = [System.Drawing.Color]::FromArgb(19, 61, 45)
$green = [System.Drawing.Color]::FromArgb(31, 85, 50)
$lightGreen = [System.Drawing.Color]::FromArgb(226, 238, 224)
$gold = [System.Drawing.Color]::FromArgb(190, 165, 108)
$tan = [System.Drawing.Color]::FromArgb(213, 202, 177)
$ink = [System.Drawing.Color]::FromArgb(21, 44, 31)
$muted = [System.Drawing.Color]::FromArgb(94, 106, 82)
$white = [System.Drawing.Color]::White
$shooterBlue = [System.Drawing.Color]::FromArgb(26, 107, 154)
$gilmoreRed = [System.Drawing.Color]::FromArgb(154, 26, 26)

function New-Font($family, $size, $style = [System.Drawing.FontStyle]::Regular) {
    try { return [System.Drawing.Font]::new($family, $size, $style, [System.Drawing.GraphicsUnit]::Pixel) }
    catch { return [System.Drawing.Font]::new('Arial', $size, $style, [System.Drawing.GraphicsUnit]::Pixel) }
}

function New-RectF($x, $y, $w, $h) { return [System.Drawing.RectangleF]::new([float]$x, [float]$y, [float]$w, [float]$h) }
function New-Rect($x, $y, $w, $h) { return [System.Drawing.Rectangle]::new([int]$x, [int]$y, [int]$w, [int]$h) }

function Get-RoundedPath($rect, $radius) {
    $path = [System.Drawing.Drawing2D.GraphicsPath]::new()
    $d = $radius * 2
    $path.AddArc($rect.X, $rect.Y, $d, $d, 180, 90)
    $path.AddArc($rect.Right - $d, $rect.Y, $d, $d, 270, 90)
    $path.AddArc($rect.Right - $d, $rect.Bottom - $d, $d, $d, 0, 90)
    $path.AddArc($rect.X, $rect.Bottom - $d, $d, $d, 90, 90)
    $path.CloseFigure()
    return $path
}

function Fill-RoundedRect($g, $rect, $radius, $color) {
    $path = Get-RoundedPath $rect $radius
    $brush = [System.Drawing.SolidBrush]::new($color)
    $g.FillPath($brush, $path)
    $brush.Dispose(); $path.Dispose()
}

function Stroke-RoundedRect($g, $rect, $radius, $color, $width = 2) {
    $path = Get-RoundedPath $rect $radius
    $pen = [System.Drawing.Pen]::new($color, $width)
    $g.DrawPath($pen, $path)
    $pen.Dispose(); $path.Dispose()
}

function Draw-Text($g, $text, $font, $color, $x, $y, $w, $h, $align = 'Near', $valign = 'Near') {
    $brush = [System.Drawing.SolidBrush]::new($color)
    $sf = [System.Drawing.StringFormat]::new()
    $sf.Alignment = [System.Drawing.StringAlignment]::$align
    $sf.LineAlignment = [System.Drawing.StringAlignment]::$valign
    $sf.Trimming = [System.Drawing.StringTrimming]::EllipsisCharacter
    $sf.FormatFlags = $sf.FormatFlags -bor [System.Drawing.StringFormatFlags]::NoClip -bor [System.Drawing.StringFormatFlags]::NoWrap
    $g.DrawString($text, $font, $brush, (New-RectF $x $y $w $h), $sf)
    $sf.Dispose(); $brush.Dispose()
}

function Draw-Table($g, $x, $y, $w, $title, $headers, $rows, $colWeights, $rowH, $fontSize = 23) {
    $titleFont = New-Font 'Georgia' 34 ([System.Drawing.FontStyle]::Bold)
    $headFont = New-Font 'Arial' 20 ([System.Drawing.FontStyle]::Bold)
    $cellFont = New-Font 'Arial' $fontSize ([System.Drawing.FontStyle]::Regular)
    $boldFont = New-Font 'Arial' $fontSize ([System.Drawing.FontStyle]::Bold)
    $pad = 12
    $headerH = 42
    $titleH = 52
    $h = $titleH + $headerH + ($rows.Count * $rowH)
    Fill-RoundedRect $g (New-Rect $x $y $w $h) 24 $white
    Stroke-RoundedRect $g (New-Rect $x $y $w $h) 24 $tan 2
    Fill-RoundedRect $g (New-Rect $x $y $w $titleH) 24 $deepGreen
    Draw-Text $g $title $titleFont $cream $x $y $w $titleH 'Center' 'Center'

    $total = 0; foreach ($cw in $colWeights) { $total += $cw }
    $colXs = @($x)
    $running = $x
    foreach ($cw in $colWeights) { $running += [math]::Round($w * $cw / $total); $colXs += $running }
    $colXs[$colXs.Count - 1] = $x + $w

    $hy = $y + $titleH
    $headBrush = [System.Drawing.SolidBrush]::new($green)
    $g.FillRectangle($headBrush, (New-Rect $x $hy $w $headerH)); $headBrush.Dispose()
    for ($i = 0; $i -lt $headers.Count; $i++) {
        Draw-Text $g $headers[$i] $headFont $cream ($colXs[$i] + $pad) $hy (($colXs[$i+1] - $colXs[$i]) - (2*$pad)) $headerH 'Near' 'Center'
    }

    $linePen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(232, 228, 220), 1)
    for ($r = 0; $r -lt $rows.Count; $r++) {
        $ry = $hy + $headerH + ($r * $rowH)
        if ($r % 2 -eq 0) {
            $b = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(250, 248, 244))
            $g.FillRectangle($b, (New-Rect $x $ry $w $rowH)); $b.Dispose()
        }
        $g.DrawLine($linePen, $x, $ry + $rowH, $x + $w, $ry + $rowH)
        for ($c = 0; $c -lt $headers.Count; $c++) {
            $txt = [string]$rows[$r][$c]
            $color = $ink
            $font = $cellFont
            if ($txt -match 'Shooter') { $color = $shooterBlue; $font = $boldFont }
            elseif ($txt -match 'Gilmore') { $color = $gilmoreRed; $font = $boldFont }
            elseif ($txt -match '^\$|Bandon Dues|Winner|1st|800') { $font = $boldFont }
            Draw-Text $g $txt $font $color ($colXs[$c] + $pad) ($ry + 2) (($colXs[$c+1] - $colXs[$c]) - (2*$pad)) ($rowH - 4) 'Near' 'Center'
        }
    }
    $linePen.Dispose()
    $titleFont.Dispose(); $headFont.Dispose(); $cellFont.Dispose(); $boldFont.Dispose()
    return $h
}

$bmp = [System.Drawing.Bitmap]::new($W, $H)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit
$g.Clear($cream)

# Subtle background texture / golf contours
$contourPen = [System.Drawing.Pen]::new([System.Drawing.Color]::FromArgb(34, 31, 85, 50), 2)
for ($i = -4; $i -lt 9; $i++) {
    $rect = New-Rect (-200 + $i*170) (120 + $i*120) 1100 520
    $g.DrawEllipse($contourPen, $rect)
}
$contourPen.Dispose()

# Logo
if (Test-Path $logoPath) {
    $logo = [System.Drawing.Image]::FromFile($logoPath)
    $logoSize = 270
    $logoX = [int](($W - $logoSize) / 2)
    $g.DrawImage($logo, (New-Rect $logoX 55 $logoSize $logoSize))
    $logo.Dispose()
}

# Hero card
$heroX = 90; $heroY = 350; $heroW = $W - 180; $heroH = 245
Fill-RoundedRect $g (New-Rect $heroX $heroY $heroW $heroH) 28 $deepGreen
# simple diagonal overlay
$overlayBrush = [System.Drawing.Drawing2D.LinearGradientBrush]::new((New-Rect $heroX $heroY $heroW $heroH), [System.Drawing.Color]::FromArgb(65, 214, 189, 123), [System.Drawing.Color]::FromArgb(0, 214, 189, 123), 25)
$g.FillRectangle($overlayBrush, (New-Rect $heroX $heroY $heroW $heroH)); $overlayBrush.Dispose()
Stroke-RoundedRect $g (New-Rect $heroX $heroY $heroW $heroH) 28 $gold 3
$titleFont = New-Font "Georgia" 88 ([System.Drawing.FontStyle]::Bold)
$subFont = New-Font "Arial" 27 ([System.Drawing.FontStyle]::Bold)
Draw-Text $g "THE BATTLE AT BANDON" $titleFont $cream $heroX ($heroY+42) $heroW 105 "Center" "Center"
Draw-Text $g "THE 6TH ANNUAL CHUBBS PETERSON INVITATIONAL  •  JUNE 17–20, 2026" $subFont $gold $heroX ($heroY+145) $heroW 48 "Center" "Center"
Draw-Text $g "FAKE HAND. REAL GAME.  •  ITS ALL IN THE HIPS." (New-Font "Arial" 21 ([System.Drawing.FontStyle]::Bold)) $cream $heroX ($heroY+190) $heroW 34 "Center" "Center"
$titleFont.Dispose(); $subFont.Dispose()

# Top summary tiles
$tileY = 625; $tileH = 100; $tileW = 370; $gap = 34; $startX = 90
$tiles = @(
    @("Team Championship", "`$500/player • First to 8.5"),
    @("Individual Championship", "`$500 • Net Stableford"),
    @("OG Belt", "`$750 • Gross Stableford"),
    @("Skins", "`$100/round • `$800 pot")
)
for ($i=0; $i -lt $tiles.Count; $i++) {
    $tx = $startX + $i * ($tileW + $gap)
    Fill-RoundedRect $g (New-Rect $tx $tileY $tileW $tileH) 18 $white
    Stroke-RoundedRect $g (New-Rect $tx $tileY $tileW $tileH) 18 $tan 2
    Draw-Text $g $tiles[$i][0] (New-Font "Arial" 22 ([System.Drawing.FontStyle]::Bold)) $green ($tx+18) ($tileY+14) ($tileW-36) 30 "Center" "Center"
    Draw-Text $g $tiles[$i][1] (New-Font "Arial" 24 ([System.Drawing.FontStyle]::Bold)) $ink ($tx+18) ($tileY+52) ($tileW-36) 34 "Center" "Center"
}

$scheduleRows = @(
    @("1","17-Jun","8:40 AM","Scramble MP","Sheep Ranch","Cutshaw (7) + Joe D (7) = team 4","Haynes (3) + Hage (9) = team 2","Shooter +2"),
    @("2","17-Jun","8:50 AM","Scramble MP","Sheep Ranch","Pat D (5) + Phillips (15) = team 4","Hedges (12) + Vandercar (-2) = team 1","Shooter +3"),
    @("3","17-Jun","2:40 PM","Best Ball Stroke","Pacific Dunes","Cutshaw (7) + Phillips (15)","Hage (10) + Hedges (13)","Individual"),
    @("4","17-Jun","2:50 PM","Best Ball Stroke","Pacific Dunes","Pat D (5) + Joe D (7)","Vandercar (-2) + Haynes (3)","Individual"),
    @("5","18-Jun","9:30 AM","Mod Alt MP","Bandon Dunes","Cutshaw (7) + Pat D (5) = team 6","Hedges (12) + Haynes (2) = team 6","Even"),
    @("6","18-Jun","9:40 AM","Mod Alt MP","Bandon Dunes","Phillips (15) + Joe D (7) = team 10","Vandercar (-2) + Hage (9) = team 2","Shooter +8"),
    @("7","18-Jun","3:45 PM","Scramble MP","Shortys","Cutshaw + Joe","Hage + Vandercar","No HCP"),
    @("8","18-Jun","4:00 PM","Scramble MP","Shortys","Pat D + Phillips","Hedges + Haynes","No HCP"),
    @("9","19-Jun","10:40 AM","Best Ball Stroke","Old Macdonald","Cutshaw (7) + Phillips (14)","Haynes (2) + Hage (9)","Individual"),
    @("10","19-Jun","10:50 AM","Best Ball Stroke","Old Macdonald","Pat D (5) + Joe D (7)","Hedges (12) + Vandercar (-2)","Individual"),
    @("11","19-Jun","5:00 PM","Alt Shot MP","Bandon Preserve","Cutshaw (2) + Pat D (1) = team 2","Haynes (-1) + Vandercar (-5) = team -3","Shooter +5"),
    @("12","19-Jun","5:15 PM","Alt Shot MP","Bandon Preserve","Phillips (8) + Joe D (2) = team 5","Hedges (6) + Hage (4) = team 5","Even"),
    @("13","20-Jun","11:00 AM","Singles MP","Bandon Trails","Pat Donoho (6)","Vandercar (-1)","Shooter +7"),
    @("14","20-Jun","11:00 AM","Singles MP","Bandon Trails","Ryan Phillips (16)","James Hedges (13)","Shooter +3"),
    @("15","20-Jun","11:10 AM","Singles MP","Bandon Trails","Joe Donoho (8)","Adam Hage (10)","Gilmore +2"),
    @("16","20-Jun","11:10 AM","Singles MP","Bandon Trails","Chris Cutshaw (8)","Mike Haynes (3)","Shooter +5")
)
Draw-Table $g 90 765 1620 "Tournament Schedule & Match Strokes" @("#","Date","Tee","Format / Play","Course","Team Shooter (Course HCP)","Team Gilmore (Course HCP)","Strokes") $scheduleRows @(0.35,0.7,0.85,1.25,1.3,3.05,3.1,1.05) 43 16 | Out-Null

$feesRows = @(
    @("Room pp 4 nights @ `$300","`$1,200.00"),
    @("Morning Tees x4 @ `$375","`$1,500.00"),
    @("Replay Tee x1 @ `$190","`$190.00"),
    @("Short Course x2 @ `$125","`$250.00"),
    @("Bandon Dues","`$3,140.00")
)
Draw-Table $g 90 1590 520 "Trip Fees" @("Fee Type","Amount") $feesRows @(2.5,1.0) 44 19 | Out-Null

$playerRows = @(
    @("Vandercar","Gilmore","-0.2"),
    @("Haynes","Gilmore","3.5"),
    @("Pat Donoho","Shooter","5.9"),
    @("Joe Donoho","Shooter","7.4"),
    @("Cutshaw","Shooter","7.7"),
    @("Hage","Gilmore","9.5"),
    @("Hedges","Gilmore","12.2"),
    @("Phillips","Shooter","14.3")
)
Draw-Table $g 90 1920 520 "Players" @("Player","Team","Handicap") $playerRows @(1.55,1.0,0.85) 35 20 | Out-Null

$compRows = @(
    @("Team Champ","`$500/player","Winner Takes All (`$4,000)","Match play, 16 pts, first to 8.5"),
    @("Individual","`$500/player","1st `$2,000 · 2nd `$1,250 · 3rd `$750","NET Stableford, 3 rounds"),
    @("OG Belt","`$750/player","1st `$2,000 · 2nd `$1,000","Gross Stableford + team bonus"),
    @("Skins","`$100/round","`$800 pot split per skin","NET par next hole to collect")
)
Draw-Table $g 650 1590 1060 "Competitions & Payouts" @("Competition","Buy-in","Payouts","Scoring") $compRows @(1.35,1.0,2.55,2.45) 54 18 | Out-Null

# Footer
Draw-Text $g "Welcome to Bandon. Pairings, buy-ins, handicaps, and formats are locked." (New-Font "Georgia" 26 ([System.Drawing.FontStyle]::Bold)) $green 650 2102 1060 50 "Center" "Center"
Draw-Text $g "Save this card for quick reference throughout the week." (New-Font "Arial" 22 ([System.Drawing.FontStyle]::Regular)) $muted 650 2150 1060 34 "Center" "Center"

# Save
$bmp.Save($outPath, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()
Write-Host "Created $outPath"
