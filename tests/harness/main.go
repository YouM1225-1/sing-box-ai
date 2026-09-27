package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/netip"
	"os"
	"path/filepath"

	"github.com/sagernet/sing-box/adapter"
	"github.com/sagernet/sing-box/common/srs"
	"github.com/sagernet/sing-box/option"
	"github.com/sagernet/sing-box/route/rule"
	SJ "github.com/sagernet/sing/common/json"
	M "github.com/sagernet/sing/common/metadata"
)

type Case struct {
	Name, File, Source, Destination, Domain, FQDN string
	Want                                      bool
}

func check(err error) {
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: match-harness cases.json")
		os.Exit(2)
	}
	data, err := os.ReadFile(os.Args[1])
	check(err)
	var cases []Case
	check(json.Unmarshal(data, &cases))
	if len(cases) == 0 {
		check(fmt.Errorf("empty case set"))
	}
	cache := make(map[string][]adapter.HeadlessRule)
	failures := 0
	for _, c := range cases {
		rules, ok := cache[c.File]
		if !ok {
			content, err := os.ReadFile(filepath.Join(filepath.Dir(os.Args[1]), c.File))
			check(err)
			var parsed option.PlainRuleSetCompat
			if filepath.Ext(c.File) == ".srs" {
				parsed, err = srs.Read(bytes.NewReader(content), false)
			} else {
				parsed, err = SJ.UnmarshalExtended[option.PlainRuleSetCompat](content)
			}
			check(err)
			for _, opts := range parsed.Options.Rules {
				r, err := rule.NewHeadlessRule(context.Background(), opts)
				check(err)
				rules = append(rules, r)
			}
			cache[c.File] = rules
		}
		matched := false
		for _, r := range rules {
			// Matching mutates caches in metadata; never share it between cases/branches.
			metadata := adapter.InboundContext{Domain: c.Domain}
			if c.Source != "" {
				metadata.Source = M.Socksaddr{Addr: netip.MustParseAddr(c.Source), Port: 12345}
			}
			if c.Destination != "" {
				metadata.Destination = M.Socksaddr{Addr: netip.MustParseAddr(c.Destination), Port: 443}
			}
			if c.FQDN != "" {
				metadata.Destination = M.Socksaddr{Fqdn: c.FQDN, Port: 443}
			}
			if r.Match(&metadata) {
				matched = true
				break
			}
		}
		if matched != c.Want {
			failures++
		}
		check(json.NewEncoder(os.Stdout).Encode(map[string]any{"name": c.Name, "file": c.File, "expected": c.Want, "actual": matched, "pass": matched == c.Want}))
	}
	fmt.Fprintf(os.Stderr, "cases=%d failures=%d\n", len(cases), failures)
	if failures != 0 {
		os.Exit(1)
	}
}
