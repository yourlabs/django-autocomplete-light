<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="content-type" content="text/html;charset=utf-8">
  <title>autocomplete.js</title>
  <link rel="stylesheet" href="../../../docs/source/_static/pycco.css">
</head>
<body>
<div id="background"></div>
<div id='container'>
  <div class='section'>
    <div class='docs'><h1>autocomplete.js</h1></div>
  </div>
  <div class='clearall'>
  <div class='section' id='section-0'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-0'>#</a>
      </div>
      <p>The autocomplete class constructor. Basically it takes a takes a text input
element as argument, and sets attributes and methods for this instance.</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre><span class="kd">function</span> <span class="nx">Autocomplete</span><span class="p">(</span><span class="nx">el</span><span class="p">)</span> <span class="p">{</span></pre></div>
    </div>
  </div>
  <div class='clearall'></div>
  <div class='section' id='section-1'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-1'>#</a>
      </div>
      <p>The text input element that should have the suggestion box.</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre>    <span class="k">this</span><span class="p">.</span><span class="nx">el</span> <span class="o">=</span> <span class="nx">el</span><span class="p">;</span></pre></div>
    </div>
  </div>
  <div class='clearall'></div>
  <div class='section' id='section-2'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-2'>#</a>
      </div>
      <p>Disable browser's autocomplete on that element.</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre>    <span class="k">this</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">attr</span><span class="p">(</span><span class="s1">&#39;autocomplete&#39;</span><span class="p">,</span> <span class="s1">&#39;off&#39;</span><span class="p">);</span></pre></div>
    </div>
  </div>
  <div class='clearall'></div>
  <div class='section' id='section-3'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-3'>#</a>
      </div>
      <p>Sets the initial value to an empty string.</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre>    <span class="k">this</span><span class="p">.</span><span class="nx">value</span> <span class="o">=</span> <span class="s1">&#39;&#39;</span><span class="p">;</span></pre></div>
    </div>
  </div>
  <div class='clearall'></div>
  <div class='section' id='section-4'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-4'>#</a>
      </div>
      <p>Current XMLHttpRequest that is kept so that when another request is
started, a unfinished request is aborted. This avoids having several
ajax requests at the time.</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre>    <span class="k">this</span><span class="p">.</span><span class="nx">xhr</span> <span class="o">=</span> <span class="kc">false</span><span class="p">;</span></pre></div>
    </div>
  </div>
  <div class='clearall'></div>
  <div class='section' id='section-5'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-5'>#</a>
      </div>
      <p>Url of the autocomplete view, that should parse the queryVariable and
return a rendered autocomplete box.</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre>    <span class="k">this</span><span class="p">.</span><span class="nx">url</span> <span class="o">=</span> <span class="kc">false</span><span class="p">;</span></pre></div>
    </div>
  </div>
  <div class='clearall'></div>
  <div class='section' id='section-6'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-6'>#</a>
      </div>
      <p>Time to wait after a key was pressed in the text input before firing an
ajax request.</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre>    <span class="k">this</span><span class="p">.</span><span class="nx">timeout</span> <span class="o">=</span> <span class="mi">100</span><span class="p">;</span></pre></div>
    </div>
  </div>
  <div class='clearall'></div>
  <div class='section' id='section-7'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-7'>#</a>
      </div>
      <p>The id of this autocomplete instance. It should be unique as it is used
as key by the plugin registry of Autocomplete instances.</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre>    <span class="k">this</span><span class="p">.</span><span class="nx">id</span> <span class="o">=</span> <span class="kc">false</span><span class="p">;</span></pre></div>
    </div>
  </div>
  <div class='clearall'></div>
  <div class='section' id='section-8'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-8'>#</a>
      </div>
      <p>Fire the autocomplete after that number of characters is in the
autocomplete.</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre>    <span class="k">this</span><span class="p">.</span><span class="nx">minCharacters</span> <span class="o">=</span> <span class="mi">2</span><span class="p">;</span></pre></div>
    </div>
  </div>
  <div class='clearall'></div>
  <div class='section' id='section-9'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-9'>#</a>
      </div>
      <p>Text input default text, used as a placeholder.</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre>    <span class="k">this</span><span class="p">.</span><span class="nx">defaultValue</span> <span class="o">=</span> <span class="s1">&#39;type your search here&#39;</span><span class="p">;</span></pre></div>
    </div>
  </div>
  <div class='clearall'></div>
  <div class='section' id='section-10'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-10'>#</a>
      </div>
      <p>Class of the currently hovered element.</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre>    <span class="k">this</span><span class="p">.</span><span class="nx">activeClass</span> <span class="o">=</span> <span class="s1">&#39;active&#39;</span><span class="p">;</span></pre></div>
    </div>
  </div>
  <div class='clearall'></div>
  <div class='section' id='section-11'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-11'>#</a>
      </div>
      <p>A selector that matches all options of the autocomplete.</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre>    <span class="k">this</span><span class="p">.</span><span class="nx">iterablesSelector</span> <span class="o">=</span> <span class="s1">&#39;li:has(a)&#39;</span><span class="p">;</span></pre></div>
    </div>
  </div>
  <div class='clearall'></div>
  <div class='section' id='section-12'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-12'>#</a>
      </div>
      <p>Name of the variable to pass to the Autocomplete url. For example, if
the text input contains 'abc' then it will fetch the autocomplete box
from this url
this.url + '?' + this.queryVariable + '=abc'.</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre>    <span class="k">this</span><span class="p">.</span><span class="nx">queryVariable</span> <span class="o">=</span> <span class="s1">&#39;q&#39;</span><span class="p">;</span></pre></div>
    </div>
  </div>
  <div class='clearall'></div>
  <div class='section' id='section-13'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-13'>#</a>
      </div>
      <p>Milliseconds after which the script should check if the autocomplete box
should be hidden</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre>    <span class="k">this</span><span class="p">.</span><span class="nx">blurTimeout</span> <span class="o">=</span> <span class="mi">500</span><span class="p">;</span></pre></div>
    </div>
  </div>
  <div class='clearall'></div>
  <div class='section' id='section-14'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-14'>#</a>
      </div>
      <p>Where to append the autocomplete suggestion box, note that it's placed
absolutely.</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre>    <span class="k">this</span><span class="p">.</span><span class="nx">appendTo</span> <span class="o">=</span> <span class="nx">$</span><span class="p">(</span><span class="s1">&#39;body&#39;</span><span class="p">);</span></pre></div>
    </div>
  </div>
  <div class='clearall'></div>
  <div class='section' id='section-15'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-15'>#</a>
      </div>
      <p>Extra classes to add to the autocomplete box container.</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre>    <span class="k">this</span><span class="p">.</span><span class="nx">outerContainerClasses</span> <span class="o">=</span> <span class="s1">&#39;&#39;</span><span class="p">;</span></pre></div>
    </div>
  </div>
  <div class='clearall'></div>
  <div class='section' id='section-16'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-16'>#</a>
      </div>
      <p>Extra data to pass to the autocomplete url.</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre>    <span class="k">this</span><span class="p">.</span><span class="nx">data</span> <span class="o">=</span> <span class="p">{};</span></pre></div>
    </div>
  </div>
  <div class='clearall'></div>
  <div class='section' id='section-17'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-17'>#</a>
      </div>
      <p>Called after an Autocomplete was instanciated <em>and</em> overridden.</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre>    <span class="k">this</span><span class="p">.</span><span class="nx">initialize</span> <span class="o">=</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span>
        <span class="kd">var</span> <span class="nx">autocomplete</span> <span class="o">=</span> <span class="k">this</span><span class="p">;</span>

        <span class="k">this</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">val</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">defaultValue</span><span class="p">);</span>
        <span class="k">this</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">live</span><span class="p">(</span><span class="s1">&#39;focus&#39;</span><span class="p">,</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span>
            <span class="k">if</span> <span class="p">(</span><span class="nx">$</span><span class="p">(</span><span class="k">this</span><span class="p">).</span><span class="nx">val</span><span class="p">()</span> <span class="o">==</span> <span class="nx">autocomplete</span><span class="p">.</span><span class="nx">defaultValue</span><span class="p">)</span> <span class="p">{</span>
                <span class="nx">$</span><span class="p">(</span><span class="k">this</span><span class="p">).</span><span class="nx">val</span><span class="p">(</span><span class="s1">&#39;&#39;</span><span class="p">);</span>
            <span class="p">}</span>
        <span class="p">});</span>
        <span class="k">this</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">live</span><span class="p">(</span><span class="s1">&#39;blur&#39;</span><span class="p">,</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span>
            <span class="k">if</span> <span class="p">(</span><span class="nx">$</span><span class="p">(</span><span class="k">this</span><span class="p">).</span><span class="nx">val</span><span class="p">()</span> <span class="o">==</span> <span class="s1">&#39;&#39;</span><span class="p">)</span> <span class="p">{</span>
                <span class="nx">$</span><span class="p">(</span><span class="k">this</span><span class="p">).</span><span class="nx">val</span><span class="p">(</span><span class="nx">autocomplete</span><span class="p">.</span><span class="nx">defaultValue</span><span class="p">);</span>
            <span class="p">}</span>
        <span class="p">});</span>

        <span class="nx">$</span><span class="p">(</span><span class="s1">&#39;.yourlabs_autocomplete.inner_container.id_&#39;</span><span class="o">+</span><span class="k">this</span><span class="p">.</span><span class="nx">id</span><span class="o">+</span><span class="s1">&#39; &#39;</span> <span class="o">+</span> <span class="k">this</span><span class="p">.</span><span class="nx">iterablesSelector</span><span class="p">).</span><span class="nx">live</span><span class="p">({</span>
            <span class="nx">mouseenter</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">e</span><span class="p">)</span> <span class="p">{</span>
                <span class="nx">$</span><span class="p">(</span><span class="s1">&#39;.yourlabs_autocomplete.inner_container.id_&#39;</span><span class="o">+</span><span class="nx">autocomplete</span><span class="p">.</span><span class="nx">id</span><span class="o">+</span><span class="s1">&#39; &#39;</span> <span class="o">+</span> <span class="nx">autocomplete</span><span class="p">.</span><span class="nx">iterablesSelector</span> <span class="o">+</span> <span class="s1">&#39;.&#39;</span> <span class="o">+</span> <span class="nx">autocomplete</span><span class="p">.</span><span class="nx">activeClass</span><span class="p">).</span><span class="nx">each</span><span class="p">(</span><span class="kd">function</span><span class="p">()</span> <span class="p">{</span>
                    <span class="nx">autocomplete</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">trigger</span><span class="p">(</span><span class="s1">&#39;deactivateOption&#39;</span><span class="p">,</span> <span class="p">[</span><span class="nx">autocomplete</span><span class="p">,</span> <span class="nx">$</span><span class="p">(</span><span class="k">this</span><span class="p">)]);</span>
                <span class="p">});</span>
                <span class="nx">autocomplete</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">trigger</span><span class="p">(</span><span class="s1">&#39;activateOption&#39;</span><span class="p">,</span> <span class="p">[</span><span class="nx">autocomplete</span><span class="p">,</span> <span class="nx">$</span><span class="p">(</span><span class="k">this</span><span class="p">)]);</span>
            <span class="p">},</span>
            <span class="nx">mouseleave</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">e</span><span class="p">)</span> <span class="p">{</span>
                <span class="nx">autocomplete</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">trigger</span><span class="p">(</span><span class="s1">&#39;deactivateOption&#39;</span><span class="p">,</span> <span class="p">[</span><span class="nx">autocomplete</span><span class="p">,</span> <span class="nx">$</span><span class="p">(</span><span class="k">this</span><span class="p">)]);</span>
            <span class="p">},</span>
            <span class="nx">click</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">e</span><span class="p">)</span> <span class="p">{</span>
                <span class="nx">e</span><span class="p">.</span><span class="nx">preventDefault</span><span class="p">();</span>
                <span class="nx">e</span><span class="p">.</span><span class="nx">stopPropagation</span><span class="p">();</span>
                <span class="nx">autocomplete</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">trigger</span><span class="p">(</span><span class="s1">&#39;selectOption&#39;</span><span class="p">,</span> <span class="p">[</span><span class="nx">$</span><span class="p">(</span><span class="k">this</span><span class="p">)]);</span>
            <span class="p">},</span>
        <span class="p">});</span>

        <span class="k">this</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">keyup</span><span class="p">(</span><span class="kd">function</span><span class="p">(</span><span class="nx">e</span><span class="p">)</span> <span class="p">{</span> <span class="nx">autocomplete</span><span class="p">.</span><span class="nx">refresh</span><span class="p">();</span> <span class="p">});</span>

        <span class="nx">$</span><span class="p">(</span><span class="s1">&#39;&lt;div id=&quot;id_&#39;</span><span class="o">+</span><span class="k">this</span><span class="p">.</span><span class="nx">id</span><span class="o">+</span><span class="s1">&#39;&quot; class=&quot;&#39;</span><span class="o">+</span><span class="k">this</span><span class="p">.</span><span class="nx">outerContainerClasses</span><span class="o">+</span><span class="s1">&#39; yourlabs_autocomplete outer_container id_&#39;</span><span class="o">+</span><span class="k">this</span><span class="p">.</span><span class="nx">id</span><span class="o">+</span><span class="s1">&#39;&quot; style=&quot;position:absolute;z-index:&#39;</span><span class="o">+</span><span class="k">this</span><span class="p">.</span><span class="nx">zindex</span><span class="o">+</span><span class="s1">&#39;;&quot;&gt;&lt;div class=&quot;yourlabs_autocomplete id_&#39;</span><span class="o">+</span><span class="k">this</span><span class="p">.</span><span class="nx">id</span><span class="o">+</span><span class="s1">&#39;&quot;&gt;&lt;div class=&quot;yourlabs_autocomplete inner_container  id_&#39;</span><span class="o">+</span><span class="k">this</span><span class="p">.</span><span class="nx">id</span><span class="o">+</span><span class="s1">&#39;&quot; style=&quot;display:none;&quot;&gt;&lt;/div&gt;&lt;/div&gt;&lt;/div&gt;&#39;</span><span class="p">).</span><span class="nx">appendTo</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">appendTo</span><span class="p">);</span>
        <span class="k">this</span><span class="p">.</span><span class="nx">innerContainer</span> <span class="o">=</span> <span class="nx">$</span><span class="p">(</span><span class="s1">&#39;.yourlabs_autocomplete.inner_container.id_&#39;</span><span class="o">+</span><span class="k">this</span><span class="p">.</span><span class="nx">id</span><span class="p">);</span>
        <span class="k">this</span><span class="p">.</span><span class="nx">outerContainer</span> <span class="o">=</span> <span class="nx">$</span><span class="p">(</span><span class="s1">&#39;.yourlabs_autocomplete.outer_container.id_&#39;</span><span class="o">+</span><span class="k">this</span><span class="p">.</span><span class="nx">id</span><span class="p">);</span>

        <span class="k">if</span> <span class="p">(</span><span class="nb">window</span><span class="p">.</span><span class="nx">opera</span><span class="p">)</span> <span class="p">{</span>
            <span class="k">this</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">keypress</span><span class="p">(</span><span class="kd">function</span><span class="p">(</span><span class="nx">e</span><span class="p">)</span> <span class="p">{</span> <span class="nx">autocomplete</span><span class="p">.</span><span class="nx">onKeyPress</span><span class="p">(</span><span class="nx">e</span><span class="p">);</span> <span class="p">});</span>
        <span class="p">}</span> <span class="k">else</span> <span class="p">{</span>
            <span class="k">this</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">keydown</span><span class="p">(</span><span class="kd">function</span><span class="p">(</span><span class="nx">e</span><span class="p">)</span> <span class="p">{</span> <span class="nx">autocomplete</span><span class="p">.</span><span class="nx">onKeyPress</span><span class="p">(</span><span class="nx">e</span><span class="p">);</span> <span class="p">});</span>
        <span class="p">}</span>
        <span class="k">this</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">blur</span><span class="p">(</span><span class="kd">function</span><span class="p">(</span><span class="nx">e</span><span class="p">)</span> <span class="p">{</span> 
            <span class="nb">window</span><span class="p">.</span><span class="nx">setTimeout</span><span class="p">(</span><span class="kd">function</span><span class="p">()</span> <span class="p">{</span>
                <span class="nx">autocomplete</span><span class="p">.</span><span class="nx">hide</span><span class="p">();</span> 
            <span class="p">},</span> <span class="nx">autocomplete</span><span class="p">.</span><span class="nx">blurTimeout</span><span class="p">);</span>
        <span class="p">});</span></pre></div>
    </div>
  </div>
  <div class='clearall'></div>
  <div class='section' id='section-18'>
    <div class='docs'>
      <div class='octowrap'>
        <a class='octothorpe' href='#section-18'>#</a>
      </div>
      <p>this.el.dblclick(function(e) { autocomplete.show(); });</p>
    </div>
    <div class='code'>
      <div class="highlight"><pre>        <span class="k">this</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">focus</span><span class="p">(</span><span class="kd">function</span><span class="p">(</span><span class="nx">e</span><span class="p">)</span> <span class="p">{</span> <span class="nx">autocomplete</span><span class="p">.</span><span class="nx">show</span><span class="p">();</span> <span class="p">});</span>
    <span class="p">}</span>
    
    <span class="k">this</span><span class="p">.</span><span class="nx">onKeyPress</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">e</span><span class="p">)</span> <span class="p">{</span>
        <span class="kd">var</span> <span class="nx">option</span><span class="p">;</span>

        <span class="k">switch</span> <span class="p">(</span><span class="nx">e</span><span class="p">.</span><span class="nx">keyCode</span><span class="p">)</span> <span class="p">{</span>
            <span class="k">case</span> <span class="mi">27</span><span class="o">:</span> <span class="c1">//KEY_ESC:</span>
                <span class="k">this</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">val</span><span class="p">();</span>
                <span class="k">this</span><span class="p">.</span><span class="nx">hide</span><span class="p">();</span>
                <span class="k">break</span><span class="p">;</span>
            <span class="k">case</span> <span class="mi">9</span><span class="o">:</span> <span class="c1">//KEY_TAB:</span>
                <span class="k">break</span><span class="p">;</span>
            <span class="k">case</span> <span class="mi">13</span><span class="o">:</span> <span class="c1">//KEY_RETURN:</span>
                <span class="nx">option</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">innerContainer</span><span class="p">.</span><span class="nx">find</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">iterablesSelector</span> <span class="o">+</span> <span class="s1">&#39;.&#39;</span> <span class="o">+</span> <span class="k">this</span><span class="p">.</span><span class="nx">activeClass</span><span class="p">);</span>
                <span class="k">if</span> <span class="p">(</span><span class="nx">option</span><span class="p">)</span> <span class="p">{</span>
                    <span class="nx">e</span><span class="p">.</span><span class="nx">preventDefault</span><span class="p">();</span>
                    <span class="nx">e</span><span class="p">.</span><span class="nx">stopPropagation</span><span class="p">();</span>
                    <span class="k">this</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">trigger</span><span class="p">(</span><span class="s1">&#39;selectOption&#39;</span><span class="p">,</span> <span class="p">[</span><span class="nx">option</span><span class="p">]);</span>
                <span class="p">}</span>
                <span class="k">if</span><span class="p">(</span><span class="nx">e</span><span class="p">.</span><span class="nx">keyCode</span> <span class="o">===</span> <span class="mi">9</span><span class="p">){</span> <span class="k">return</span><span class="p">;</span> <span class="p">}</span>
                <span class="k">break</span><span class="p">;</span>
            <span class="k">case</span> <span class="mi">38</span><span class="o">:</span> <span class="c1">//KEY_UP:</span>
                <span class="k">this</span><span class="p">.</span><span class="nx">move</span><span class="p">(</span><span class="s1">&#39;up&#39;</span><span class="p">);</span>
                <span class="k">break</span><span class="p">;</span>
            <span class="k">case</span> <span class="mi">40</span><span class="o">:</span> <span class="c1">//KEY_DOWN:</span>
                <span class="k">this</span><span class="p">.</span><span class="nx">move</span><span class="p">(</span><span class="s1">&#39;down&#39;</span><span class="p">);</span>
                <span class="k">break</span><span class="p">;</span>
            <span class="k">default</span><span class="o">:</span>
                <span class="k">return</span><span class="p">;</span>
        <span class="p">}</span>
        <span class="nx">e</span><span class="p">.</span><span class="nx">stopImmediatePropagation</span><span class="p">();</span>
        <span class="nx">e</span><span class="p">.</span><span class="nx">preventDefault</span><span class="p">();</span>
    <span class="p">}</span>
    
    <span class="k">this</span><span class="p">.</span><span class="nx">show</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">html</span><span class="p">)</span> <span class="p">{</span>
        <span class="k">if</span> <span class="p">(</span><span class="nx">$</span><span class="p">.</span><span class="nx">trim</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">innerContainer</span><span class="p">.</span><span class="nx">html</span><span class="p">()).</span><span class="nx">length</span> <span class="o">==</span> <span class="mi">0</span> <span class="o">&amp;&amp;</span> <span class="o">!</span><span class="k">this</span><span class="p">.</span><span class="nx">xhr</span><span class="p">)</span> <span class="p">{</span>
            <span class="k">this</span><span class="p">.</span><span class="nx">fetchAutocomplete</span><span class="p">();</span>
            <span class="k">return</span><span class="p">;</span>
        <span class="p">}</span>
        
        <span class="k">if</span> <span class="p">(</span><span class="nx">html</span><span class="p">)</span> <span class="p">{</span>
            <span class="k">this</span><span class="p">.</span><span class="nx">innerContainer</span><span class="p">.</span><span class="nx">html</span><span class="p">(</span><span class="nx">html</span><span class="p">);</span>
        <span class="p">}</span>
        <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="k">this</span><span class="p">.</span><span class="nx">innerContainer</span><span class="p">.</span><span class="nx">is</span><span class="p">(</span><span class="s1">&#39;:visible&#39;</span><span class="p">))</span> <span class="p">{</span>
            <span class="k">this</span><span class="p">.</span><span class="nx">outerContainer</span><span class="p">.</span><span class="nx">show</span><span class="p">();</span>
            <span class="k">this</span><span class="p">.</span><span class="nx">innerContainer</span><span class="p">.</span><span class="nx">show</span><span class="p">();</span>
        <span class="p">}</span>
    <span class="p">}</span>
    
    <span class="k">this</span><span class="p">.</span><span class="nx">hide</span> <span class="o">=</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span>
        <span class="k">this</span><span class="p">.</span><span class="nx">outerContainer</span><span class="p">.</span><span class="nx">hide</span><span class="p">();</span>
        <span class="k">this</span><span class="p">.</span><span class="nx">innerContainer</span><span class="p">.</span><span class="nx">hide</span><span class="p">();</span>
    <span class="p">}</span>
    
    <span class="k">this</span><span class="p">.</span><span class="nx">move</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">way</span><span class="p">)</span> <span class="p">{</span>
        <span class="kd">var</span> <span class="nx">current</span><span class="p">,</span> <span class="nx">target</span><span class="p">,</span> <span class="nx">first</span><span class="p">,</span> <span class="nx">last</span><span class="p">;</span>
        <span class="nx">current</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">innerContainer</span><span class="p">.</span><span class="nx">find</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">iterablesSelector</span> <span class="o">+</span> <span class="s1">&#39;.&#39;</span> <span class="o">+</span> <span class="k">this</span><span class="p">.</span><span class="nx">activeClass</span><span class="p">);</span>
        <span class="nx">first</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">innerContainer</span><span class="p">.</span><span class="nx">find</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">iterablesSelector</span> <span class="o">+</span> <span class="s1">&#39;:first&#39;</span><span class="p">);</span>
        <span class="nx">last</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">innerContainer</span><span class="p">.</span><span class="nx">find</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">iterablesSelector</span> <span class="o">+</span> <span class="s1">&#39;:last&#39;</span><span class="p">);</span>

        <span class="k">this</span><span class="p">.</span><span class="nx">show</span><span class="p">();</span>

        <span class="k">if</span> <span class="p">(</span><span class="nx">current</span><span class="p">.</span><span class="nx">length</span><span class="p">)</span> <span class="p">{</span>
            <span class="k">if</span> <span class="p">(</span><span class="nx">way</span> <span class="o">==</span> <span class="s1">&#39;up&#39;</span><span class="p">)</span> <span class="p">{</span>
                <span class="nx">target</span> <span class="o">=</span> <span class="nx">current</span><span class="p">.</span><span class="nx">prevAll</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">iterablesSelector</span> <span class="o">+</span> <span class="s1">&#39;:first&#39;</span><span class="p">);</span>
                <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="nx">target</span><span class="p">.</span><span class="nx">length</span><span class="p">)</span> <span class="p">{</span>
                    <span class="nx">target</span> <span class="o">=</span> <span class="nx">last</span><span class="p">;</span>
                <span class="p">}</span>
            <span class="p">}</span> <span class="k">else</span> <span class="p">{</span>
                <span class="nx">target</span> <span class="o">=</span> <span class="nx">current</span><span class="p">.</span><span class="nx">nextAll</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">iterablesSelector</span> <span class="o">+</span> <span class="s1">&#39;:first&#39;</span><span class="p">);</span>
                <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="nx">target</span><span class="p">.</span><span class="nx">length</span><span class="p">)</span> <span class="p">{</span>
                    <span class="nx">target</span> <span class="o">=</span> <span class="nx">first</span><span class="p">;</span>
                <span class="p">}</span>
            <span class="p">}</span>
            <span class="k">this</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">trigger</span><span class="p">(</span><span class="s1">&#39;deactivateOption&#39;</span><span class="p">,</span> <span class="p">[</span><span class="k">this</span><span class="p">,</span> <span class="nx">current</span><span class="p">]);</span>
        <span class="p">}</span> <span class="k">else</span> <span class="p">{</span>
            <span class="k">if</span> <span class="p">(</span><span class="nx">way</span> <span class="o">==</span> <span class="s1">&#39;up&#39;</span><span class="p">)</span> <span class="p">{</span>
                <span class="nx">target</span> <span class="o">=</span> <span class="nx">last</span><span class="p">;</span>
            <span class="p">}</span> <span class="k">else</span> <span class="p">{</span>
                <span class="nx">target</span> <span class="o">=</span> <span class="nx">first</span><span class="p">;</span>
            <span class="p">}</span>
        <span class="p">}</span>
        <span class="k">this</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">trigger</span><span class="p">(</span><span class="s1">&#39;activateOption&#39;</span><span class="p">,</span> <span class="p">[</span><span class="k">this</span><span class="p">,</span> <span class="nx">target</span><span class="p">]);</span>
    <span class="p">}</span>
    
    <span class="k">this</span><span class="p">.</span><span class="nx">fixPosition</span> <span class="o">=</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span>
        <span class="kd">var</span> <span class="nx">css</span> <span class="o">=</span> <span class="p">{</span>
            <span class="s1">&#39;top&#39;</span><span class="o">:</span> <span class="nb">Math</span><span class="p">.</span><span class="nx">floor</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">offset</span><span class="p">()[</span><span class="s1">&#39;top&#39;</span><span class="p">]),</span>
            <span class="s1">&#39;left&#39;</span><span class="o">:</span> <span class="nb">Math</span><span class="p">.</span><span class="nx">floor</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">offset</span><span class="p">()[</span><span class="s1">&#39;left&#39;</span><span class="p">]),</span>
            <span class="s1">&#39;position&#39;</span><span class="o">:</span> <span class="s1">&#39;absolute&#39;</span><span class="p">,</span>
        <span class="p">}</span>
        <span class="nx">css</span><span class="p">[</span><span class="s1">&#39;top&#39;</span><span class="p">]</span> <span class="o">+=</span> <span class="nb">Math</span><span class="p">.</span><span class="nx">floor</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">innerHeight</span><span class="p">());</span>

        <span class="k">this</span><span class="p">.</span><span class="nx">outerContainer</span><span class="p">.</span><span class="nx">css</span><span class="p">(</span><span class="nx">css</span><span class="p">);</span>
    <span class="p">}</span>
    
    <span class="k">this</span><span class="p">.</span><span class="nx">refresh</span> <span class="o">=</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span>
        <span class="kd">var</span> <span class="nx">newValue</span><span class="p">;</span>
        <span class="nx">newValue</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">el</span><span class="p">.</span><span class="nx">val</span><span class="p">();</span>
        <span class="k">if</span> <span class="p">(</span><span class="nx">newValue</span> <span class="o">==</span> <span class="k">this</span><span class="p">.</span><span class="nx">defaultValue</span><span class="p">)</span> <span class="p">{</span>
            <span class="k">return</span> <span class="kc">false</span><span class="p">;</span>
        <span class="p">}</span>
        <span class="k">if</span> <span class="p">(</span><span class="nx">newValue</span><span class="p">.</span><span class="nx">length</span> <span class="o">&lt;</span> <span class="k">this</span><span class="p">.</span><span class="nx">minCharacters</span><span class="p">)</span> <span class="p">{</span>
            <span class="k">return</span> <span class="kc">false</span><span class="p">;</span>
        <span class="p">}</span>
        <span class="k">if</span> <span class="p">(</span><span class="nx">newValue</span> <span class="o">==</span> <span class="k">this</span><span class="p">.</span><span class="nx">value</span><span class="p">)</span> <span class="p">{</span>
            <span class="k">return</span> <span class="kc">false</span><span class="p">;</span>
        <span class="p">}</span>
        <span class="k">this</span><span class="p">.</span><span class="nx">value</span> <span class="o">=</span> <span class="nx">newValue</span><span class="p">;</span>
        <span class="k">this</span><span class="p">.</span><span class="nx">fetchAutocomplete</span><span class="p">();</span>
    <span class="p">}</span>
    
    <span class="k">this</span><span class="p">.</span><span class="nx">fetchAutocomplete</span> <span class="o">=</span> <span class="kd">function</span><span class="p">()</span> <span class="p">{</span>
        <span class="kd">var</span> <span class="nx">autocomplete</span><span class="p">,</span> <span class="nx">data</span><span class="p">;</span>

        <span class="k">if</span> <span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">xhr</span><span class="p">)</span> <span class="p">{</span>
            <span class="k">this</span><span class="p">.</span><span class="nx">xhr</span><span class="p">.</span><span class="nx">abort</span><span class="p">();</span>
        <span class="p">}</span>

        <span class="nx">autocomplete</span> <span class="o">=</span> <span class="k">this</span><span class="p">;</span>
        <span class="nx">data</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">data</span><span class="p">;</span>
        <span class="nx">data</span><span class="p">[</span><span class="k">this</span><span class="p">.</span><span class="nx">queryVariable</span><span class="p">]</span> <span class="o">=</span> <span class="k">this</span><span class="p">.</span><span class="nx">value</span><span class="p">;</span>
        <span class="k">this</span><span class="p">.</span><span class="nx">xhr</span> <span class="o">=</span> <span class="nx">$</span><span class="p">.</span><span class="nx">ajax</span><span class="p">(</span><span class="k">this</span><span class="p">.</span><span class="nx">url</span><span class="p">,</span> <span class="p">{</span>
            <span class="s1">&#39;data&#39;</span><span class="o">:</span> <span class="nx">data</span><span class="p">,</span>
            <span class="s1">&#39;complete&#39;</span><span class="o">:</span> <span class="kd">function</span><span class="p">(</span><span class="nx">jqXHR</span><span class="p">,</span> <span class="nx">textStatus</span><span class="p">)</span> <span class="p">{</span>
                <span class="nx">autocomplete</span><span class="p">.</span><span class="nx">fixPosition</span><span class="p">();</span>
                <span class="nx">autocomplete</span><span class="p">.</span><span class="nx">show</span><span class="p">(</span><span class="nx">jqXHR</span><span class="p">.</span><span class="nx">responseText</span><span class="p">);</span>
            <span class="p">},</span>
        <span class="p">});</span>
    <span class="p">}</span>
<span class="p">}</span>

<span class="nx">$</span><span class="p">.</span><span class="nx">fn</span><span class="p">.</span><span class="nx">yourlabs_autocomplete</span> <span class="o">=</span> <span class="kd">function</span><span class="p">(</span><span class="nx">overrides</span><span class="p">)</span> <span class="p">{</span>
    <span class="kd">var</span> <span class="nx">id</span><span class="p">;</span>
    <span class="nx">overrides</span> <span class="o">=</span> <span class="nx">overrides</span> <span class="o">?</span> <span class="nx">overrides</span> <span class="o">:</span> <span class="p">{};</span>
    <span class="nx">id</span> <span class="o">=</span> <span class="nx">overrides</span><span class="p">.</span><span class="nx">id</span> <span class="o">||</span> <span class="k">this</span><span class="p">.</span><span class="nx">attr</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">);</span>

    <span class="k">if</span> <span class="p">(</span><span class="o">!</span><span class="p">(</span><span class="nx">id</span> <span class="o">&amp;&amp;</span> <span class="k">this</span><span class="p">))</span> <span class="p">{</span>
        <span class="nx">alert</span><span class="p">(</span><span class="s1">&#39;failure: the element needs an id attribute, or an id option must be passed&#39;</span><span class="p">);</span>
        <span class="k">return</span> <span class="kc">false</span><span class="p">;</span>
    <span class="p">}</span>
    
    <span class="k">if</span> <span class="p">(</span><span class="nx">$</span><span class="p">.</span><span class="nx">fn</span><span class="p">.</span><span class="nx">yourlabs_autocomplete</span><span class="p">.</span><span class="nx">registry</span> <span class="o">==</span> <span class="kc">undefined</span><span class="p">)</span> <span class="p">{</span>
        <span class="nx">$</span><span class="p">.</span><span class="nx">fn</span><span class="p">.</span><span class="nx">yourlabs_autocomplete</span><span class="p">.</span><span class="nx">registry</span> <span class="o">=</span> <span class="p">{};</span>
    <span class="p">}</span>
    
    <span class="k">if</span> <span class="p">(</span><span class="nx">$</span><span class="p">.</span><span class="nx">fn</span><span class="p">.</span><span class="nx">yourlabs_autocomplete</span><span class="p">.</span><span class="nx">registry</span><span class="p">[</span><span class="nx">id</span><span class="p">]</span> <span class="o">==</span> <span class="kc">undefined</span><span class="p">)</span> <span class="p">{</span>
        <span class="nx">$</span><span class="p">.</span><span class="nx">fn</span><span class="p">.</span><span class="nx">yourlabs_autocomplete</span><span class="p">.</span><span class="nx">registry</span><span class="p">[</span><span class="nx">id</span><span class="p">]</span> <span class="o">=</span> <span class="k">new</span> <span class="nx">Autocomplete</span><span class="p">(</span><span class="k">this</span><span class="p">);</span>
        <span class="nx">$</span><span class="p">.</span><span class="nx">fn</span><span class="p">.</span><span class="nx">yourlabs_autocomplete</span><span class="p">.</span><span class="nx">registry</span><span class="p">[</span><span class="nx">id</span><span class="p">]</span> <span class="o">=</span> <span class="nx">$</span><span class="p">.</span><span class="nx">extend</span><span class="p">(</span><span class="nx">$</span><span class="p">.</span><span class="nx">fn</span><span class="p">.</span><span class="nx">yourlabs_autocomplete</span><span class="p">.</span><span class="nx">registry</span><span class="p">[</span><span class="nx">id</span><span class="p">],</span> <span class="nx">overrides</span><span class="p">);</span>
        <span class="nx">$</span><span class="p">.</span><span class="nx">fn</span><span class="p">.</span><span class="nx">yourlabs_autocomplete</span><span class="p">.</span><span class="nx">registry</span><span class="p">[</span><span class="nx">id</span><span class="p">].</span><span class="nx">initialize</span><span class="p">();</span>
    <span class="p">}</span>

    <span class="k">return</span> <span class="nx">$</span><span class="p">.</span><span class="nx">fn</span><span class="p">.</span><span class="nx">yourlabs_autocomplete</span><span class="p">.</span><span class="nx">registry</span><span class="p">[</span><span class="nx">id</span><span class="p">];</span>
<span class="p">};</span>

<span class="nx">$</span><span class="p">(</span><span class="nb">document</span><span class="p">).</span><span class="nx">ready</span><span class="p">(</span><span class="kd">function</span><span class="p">()</span> <span class="p">{</span>
    <span class="nx">$</span><span class="p">(</span><span class="nb">document</span><span class="p">).</span><span class="nx">bind</span><span class="p">(</span><span class="s1">&#39;activateOption&#39;</span><span class="p">,</span> <span class="kd">function</span><span class="p">(</span><span class="nx">e</span><span class="p">,</span> <span class="nx">autocomplete</span><span class="p">,</span> <span class="nx">option</span><span class="p">)</span> <span class="p">{</span>
        <span class="nx">option</span><span class="p">.</span><span class="nx">addClass</span><span class="p">(</span><span class="nx">autocomplete</span><span class="p">.</span><span class="nx">activeClass</span><span class="p">);</span>
    <span class="p">});</span>
    <span class="nx">$</span><span class="p">(</span><span class="nb">document</span><span class="p">).</span><span class="nx">bind</span><span class="p">(</span><span class="s1">&#39;deactivateOption&#39;</span><span class="p">,</span> <span class="kd">function</span><span class="p">(</span><span class="nx">e</span><span class="p">,</span> <span class="nx">autocomplete</span><span class="p">,</span> <span class="nx">option</span><span class="p">)</span> <span class="p">{</span>
        <span class="nx">option</span><span class="p">.</span><span class="nx">removeClass</span><span class="p">(</span><span class="nx">autocomplete</span><span class="p">.</span><span class="nx">activeClass</span><span class="p">);</span>
    <span class="p">});</span>
<span class="p">});</span>

</pre></div>
    </div>
  </div>
  <div class='clearall'></div>
</div>
</body>
