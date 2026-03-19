use Cwd qw(abs_path);

my $style = abs_path('index.ist');
$makeindex = qq(makeindex -s "$style" %O -o %D %S);
