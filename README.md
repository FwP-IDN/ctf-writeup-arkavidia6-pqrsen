# Writeup Arkavidia -- pqrsen

Kategori: Crypto


Desc singkat: diberikan sebuah kodingan, pubkey, dan ciphertext kemudian decrypt ciphertext. Pada pubkey terdapat informasi tambahan.

Berikut adalah kodingan yang diberikan

```
from Crypto.Util.number import *
from secret import *

m = bytes_to_long(flag)
p = getPrime(2048)
q = getPrime(2048)
r = inverse(pow(p, 3), q)
s = (pow(p, 2, p * q) - pow(q, 0x10001, p * q)) % (p * q)
e = 0x10001
n = p * q
assert(m < n)
c = (pow(r * m, e, n) * inverse(s, n)) % n
c = pow(c, 2, n)

open("pub.key", "w").writelines(map(lambda x: x + "\n", map(str, [r, s, e, n])))
open("flag.enc", "w").write(str(c))

```

Kita dapat menyimpelkannya menjadi persamaan.

m: unknown

p: unknown

q: unknown

n = p × q

e = 65537

r ≡ p<sup>-3</sup> mod q

s ≡ (p<sup>2</sup> - q<sup>e</sup>) mod n

c ≡ ((r×m)<sup>e</sup> × (s<sup>-1</sup>))<sup>2</sup> mod n

Untuk kesimpelan, kita dapat mengabaikan modulo untuk sementara.

Pertama-tama kita uraikan si-"c" untuk menghilangkan "dependensi"

c = ((r×m)<sup>e</sup> × (s<sup>-1</sup>))<sup>2</sup> = (r×m)<sup>e×2</sup> × (s<sup>-2</sup>)

Kemudian kita kita kalikan c dengan s<sup>2</sup> untuk mengurangi "keruwetan"

c1 = c × s<sup>2</sup> = (r×m)<sup>e×2</sup>

c1 seharusnya dapat diselesaikan dengan decrypt RSA biasa. Namun kita membutuhkan p dan q bagaimana mencarinya?

perlu diketahui bahwa pangkat dari p pada variabel r adalah minus 3 sementara pangkat dari variabel p pada s adalah 2. Jika kita kalikan r<sup>2</sup> × s<sup>3</sup> =  p<sup>-6</sup> × (p<sup>2</sup> - q<sup>e</sup>)<sup>3</sup> = (1 - q<sup>e</sup> × p<sup>-2</sup><sup>3</sup> ≡ 1 mod q

Dari sini kita dapat simpulkan bahwa r<sup>2</sup> × s<sup>3</sup>  ≡ 1 mod q sehingga GCD(r<sup>2</sup> × s<sup>3</sup> - 1, n) = q


setelah mendapat q, p = n / q

Dan dari c1 = (r×m)<sup>e×2</sup> = ((r×m)<sup>2</sup>)<sup>e</sup>, dengan RSA decryption, kita mendapatkan c2 = RSA_decrypt(c1) = (r×m)<sup>2</sup>. 

c2 = r<sup>2</sup> × m<sup>2</sup>

Kemudian kita invers r<sup>2</sup> dan dikalikan c2 untuk mendapatkan m<sup>2</sup>. Cari akar pangkat 2 dari m<sup>2</sup> dan mendapatkan m. (NB: cara ini tidak berkali jika m > min(p, q)).

Berikut adalah full solvernya. 

```
from Crypto.Util.number import *


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = egcd(b % a, a)
        print('>', a, b, (gcd, y - (b // a) * x, x))
        return (gcd, y - (b // a) * x, x)


def egcd_no_rek(a, b):
    params = [(a, b)]
    rets = None
    while True:
        a, b = params[-1]
        if a == 0:
            rets = (b, 0, 1)
            break
        else:
            params.append((b % a, a))

    while len(params) > 1:
        params.pop()
        gcd, x, y = rets
        a, b = params[-1]
        rets = (gcd, y - (b // a) * x, x)
        # print('<', a, b, rets)
    return rets


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def GCD(x, y):
    cnt = 1
    while(y):
        x, y = y, x % y
        cnt += 1

    return x


r = 4520406022113039033657660797162939630289138500452333431244873369434440664917008654897926233935194669260936436455244228292412712847458147055165510218054741905615263945946637832832474380452401356829060691391888781491763564103102803328172684122489235876631438689323669900569105862101436109131401639437033115356023889864262689841046775851622264182998320392778709236203356164011564852021539423890817980207234882732572827664693321059345770957969552067994796559435493708388852081997370753299276535661719382749269516320997096180789720805357362063969949877937372683054231428752364018201113979362600634520696143886015353446918
s = 210952290495367602268616895982972599031200132906313887226486821072874378758034586854282094671706624747631035431643443157626234559548745008941208264826136708060797428215104753972529287881309969075042431651618647651106699969299793623200197197478946584240569412689182143376699571385050827231259294378432036621427586358234519713570666980215846281250414988689002518151354369850967900220115721254217660717953891129995006983905002778641755620665015487461127265545964324220870752418511996986712750475795714561109758686181591876309400722883477076036998446843787873751513865028510876067984080387733440408094288496544583866455806039532448562808119105695055938476482462693834747148680586181729370299792989102508351853542691442745087051011677575944015800940989899841122383946046989719630196566131146237095380779980480740309765453044715672668138949416258329764265416597906803598636992282053227425523198556492674861608240276905942450143489707230326751433464956906062037346784814331256488610451652934330564990733516058339368115128690402448882684194339706923624325556499301700581227791349733065021361683887908638184473153529767736840784676636432066407196260973735476880136149922385256668463797431841369243860766211439977281057503210720653648776436940
e = 65537
n = 363183807678730330621932072016023534913614801355548670100329135533523339012177003178025658060085245778638065470114110088430501429894079257135607913463361515711563905204350190852967558093739941913613200360344652648122321660260062285556790159565545991804273063209398906236971180252545797010882936217042053304253927968460481303828598056384361633956694835950232493362443567848916913202959713886631951991301009515132037837067528809094943792636618184045856320208311127068293995599298785472394146237972911143920838826466951834384199052384195322290214695959343544513505198355788126851078299300318803567204920314035273779985028018009048778990249684441261658603517016395829552886856874647951063158258092670622871197385790918798398319541353452215643393298737163016937867716104733950717418816777254996888953343043593723193701630098349694746320044190989767597669573768170290210893971987649657150535557210197590241058699519367120002116264613637156945167103150436202018353997386573974532871485136419857550240558248023100082249302411284170276846168188843534479629303772070135998273706484879360709706063378250179662375757971656931902552964489245081803704936745721645231513615497115049776621952287806382393469186771948254798814054051026775741414208191
c = 30150132948409575857310380280068763814044945383035646852665322540585289661572001343327674032808915718561872846021039974155963579000019957062119587685431642188678401024533708445769878095807445875516609615797368046811868431951768626495767147640876719650280303345846874167225048031082762239807411352965814961212690945667072820013430926061713626115852278517175213870518617709728597235783493420386573862173254894395574140120296607224045047650343915552128997429353727097965775392888077074844329013440667148392526975039358068843189660977218211392375134779242905766699317475882932441832759520926672560157381166525303013347034858008662679249278411625780928903673688163455124528008765460186644684201738308011554868719186155552602945429538822733985615810963625319358506593538839183827783419504735637258269329251543270483862001182328809605169200585212844384352687899584090916967127491258882374899033859375520392059819864406363546993761189242905361000029904884398924427391934048317780913511231021077458027566114309338684559488310734502817156051300405892795850956835454456219333724749769012510305114294317203955483735106424998749676899393807351386694490312124345495245614695729434193104726798601065302353887915620005578365622190759919009876399568

q = GCD(n, (s**3 * r**2) - 1)
assert n % q == 0
p = n // q


gcd, yp, yq = egcd_no_rek(p, q)

assert yp * p + yq * q == 1
print((p + 1) % 4)
print((q + 1) % 4)


# c = (pow(r * m, e, n) * inverse(s, n)) % n
# c = pow(c, 2, n)

c *= pow(s, 2, n)
c %= n

inv_r = inverse(r, n)

c *= pow(inv_r, e * 2, n)
c %= n

tot = (p - 1) * (q - 1)
d = modinv(e, tot)

m2 = pow(c, d, n)


def floorSqrt(x):

    # Base cases
    if (x == 0 or x == 1):
        return x

    # Do Binary Search for floor(sqrt(x))
    start = 1
    end = x
    while (start <= end):
        mid = (start + end) // 2

        # If x is a perfect square
        if (mid * mid == x):
            return mid

        # Since we need floor, we update
        # answer when mid*mid is smaller
        # than x, and move closer to sqrt(x)
        if (mid * mid < x):
            start = mid + 1
            ans = mid

        else:

            # If mid*mid is greater than x
            end = mid - 1

    return ans


m = floorSqrt(m2)
assert m * m == m2
print(long_to_bytes(m))
```